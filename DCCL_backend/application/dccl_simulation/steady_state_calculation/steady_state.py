import numpy as np
import time
import cupy as cp
from ..utils import cal_overlap
from ..utils import cal_trans_factor
from .one_roundtrip_distribution import one_roundtrip_distribution
from ..utils import para_FFT


def steady_state(H_fsdf, H_fsf, B_aper, B_CatEye1, B_CatEye2, B_CatEye3, r1, r2, r3, P_in, lambda_,eta_c):
    # 开始计时
    start_time = time.time()
    # 经过的时间
    elapsed_time = 0

    U_M1pre = 1  # M1初始场分布
    U_M2pre = 0  # M2初始场分布
    [firstU1, firstU2, _] = one_roundtrip_distribution(U_M1pre, U_M2pre, H_fsdf, H_fsf, B_aper, B_CatEye1, B_CatEye2,
                                                       B_CatEye3, r1, r2, r3, P_in, lambda_,eta_c)
    tempU1 = firstU1
    tempU2 = firstU2
    # print(type(tempU1))
    # print(type(tempU2))
    t = 1
    _, _, _, _, delta, _ = para_FFT(0.012)

    c = float('inf')
    data={}
    while c > 0.0001:

        [s_it1, s_it2, U2] = one_roundtrip_distribution(tempU1, tempU2, H_fsdf, H_fsf, B_aper, B_CatEye1, B_CatEye2,
                                                        B_CatEye3, r1, r2, r3, P_in, lambda_,eta_c)
        
        a1 = cp.sum(cp.abs(cp.abs(s_it1) - cp.abs(tempU1)))
        b1 = cp.sum(cp.abs(tempU1))
        c1 = a1 / b1

        a2 = cp.sum(cp.abs(cp.abs(s_it2) - cp.abs(tempU2)))
        b2 = cp.sum(cp.abs(tempU2))
        c2 = a2 / b2
        del a1, a2, b1, b2
        v1 = cal_trans_factor(s_it1, tempU1)
        v2 = cal_trans_factor(s_it2, tempU2)
        # phase_shift = np.exp(-1j * np.angle(cal_overlap(s_it1, tempU1, delta)))
        # tempU1 = s_it1 * phase_shift
        tempU1=s_it1
        # phase_shift = np.exp(-1j * np.angle(cal_overlap(s_it2, tempU2, delta)))
        # tempU2 = s_it2 * phase_shift
        tempU2=s_it2
        c = c1
       

        U = U2
        R = 1 - r3 ** 2
        epsilon = 8.854187817e-12
        c0 = 3e8
        Iten_out = R * 0.5 * (epsilon * c0) * cp.abs(U) ** 2  # 电场的振幅分布转化为光强分布
        Pout = cp.sum(Iten_out)
        del U, U2, Iten_out 
        
        
        
        print(f'迭代次数: {t} 传输系数main: {v1} 传输系数free: {v2} 输出功率: {Pout * delta * delta}')
        # 用字典记录每次的数据
        data["iterationCount"] = t
        data["transmissionCoefficientMain"] = v1.item()
        data["transmissionCoefficientFree"] = v2.item()
        data["outputPower"] = Pout.item() * delta * delta
        data["isEnd"]=False
        yield data
        # yield f'迭代次数: {t} 主共振腔传输系数: {v1} 自由空间腔传输系数: {v2} 输出光功率: {Pout * delta * delta}'
        t += 1
        # 终止条件
        if t > 10:  # 改为10测试完整运行
            break
        if P_in < 1e-15:
            break
        del s_it1, s_it2
        # 强制释放显存
        cp.get_default_memory_pool().free_all_blocks()
        
        

    return Pout.item() *delta*delta, t, s_it1, s_it2  # 迭代终止时M1和M2上的场分布
