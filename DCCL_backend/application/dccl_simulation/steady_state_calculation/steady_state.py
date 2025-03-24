import numpy as np
import time

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
    t = 0
    _, _, _, _, delta, _ = para_FFT(0.012)

    c = float('inf')
    while c > 0.0001:
        [s_it1, s_it2, U2] = one_roundtrip_distribution(tempU1, tempU2, H_fsdf, H_fsf, B_aper, B_CatEye1, B_CatEye2,
                                                        B_CatEye3, r1, r2, r3, P_in, lambda_,eta_c)
        a1 = np.sum(np.abs(np.abs(s_it1) - np.abs(tempU1)))
        b1 = np.sum(np.abs(tempU1))
        c1 = a1 / b1

        a2 = np.sum(np.abs(np.abs(s_it2) - np.abs(tempU2)))
        b2 = np.sum(np.abs(tempU2))
        c2 = a2 / b2

        v1 = cal_trans_factor(s_it1, tempU1)
        v2 = cal_trans_factor(s_it2, tempU2)
        # phase_shift = np.exp(-1j * np.angle(cal_overlap(s_it1, tempU1, delta)))
        # tempU1 = s_it1 * phase_shift
        tempU1=s_it1
        # phase_shift = np.exp(-1j * np.angle(cal_overlap(s_it2, tempU2, delta)))
        # tempU2 = s_it2 * phase_shift
        tempU2=s_it2
        c = c1
        t += 1

        U = U2
        R = 1 - r3 ** 2
        epsilon = 8.854187817e-12
        c0 = 3e8
        Iten_out = R * 0.5 * (epsilon * c0) * np.abs(U) ** 2  # 电场的振幅分布转化为光强分布
        Pout = np.sum(Iten_out)

        print(f'迭代次数: {t} 传输系数main: {v1} 传输系数free: {v2} 输出功率: {Pout * delta * delta}')
        yield f'迭代次数: {t} 主共振腔传输系数: {v1} 自由空间腔传输系数: {v2} 输出光功率: {Pout * delta * delta} \n\n'
        # if t % 20 == 0:
        #     # 计算从开始到现在经过的时间
        #     elapsed_time = time.time() - start_time
        #     print(elapsed_time)

        # 终止条件
        if t > 300:  # 1000
            break
        if P_in < 1e-15:
            break

    return Pout, t, s_it1, s_it2  # 迭代终止时M1和M2上的场分布
