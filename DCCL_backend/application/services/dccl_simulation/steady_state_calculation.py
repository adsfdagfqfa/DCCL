
from .utils import cal_field_transition,  operator_reflectivity, operator_transmissivity,cal_overlap,cal_trans_factor,calculate_fft_parameters
from .gain_simulation_calculation import propagation_within_gain
import cupy as cp
import scipy.constants as const
import datetime
import logging
import types,io,scipy.io as sio
import uuid
from application.utils.redis_utils import set_redis_data
logger = logging.getLogger(__name__)
def free_cavity_trans(U_pre, H_fsdf, B_CatEye2, B_CatEye3):
    U = cal_field_transition(U_pre, H_fsdf, B_CatEye2, B_CatEye3)  # M2-L3入射表面
    return U  # 返回经过自由空间腔传输后的光场分布 

def main_cavity_trans(U_pre, H_fsf, B_CatEye1, B_aper, B_CatEye2, lm,rm,P_in,lambda_,eta_c):
    # lm = 0.001  # 增益介质长度
    U = cal_field_transition(U_pre, H_fsf, B_CatEye1, B_aper)  # M1-L1入射表面
    U = propagation_within_gain(U, lm,rm, P_in, lambda_,eta_c)
    U = cal_field_transition(U, H_fsf, B_aper, B_CatEye2)  # L2出射表面-M2
    return U

def one_roundtrip_distribution(U_M1pre, U_M2pre, matrix_all,aperture_all,data,lambda_):
    r1=data['modelAttributeList'][0]['reflectivity']  # M1的反射率
    r2 = data['modelAttributeList'][4]['reflectivity']  # M2的反射率
    r3 = data['modelAttributeList'][7]['reflectivity']  # M3的反射率
    t2 = cp.sqrt(1 - r2 ** 2)  # 透射光强率
    P_in=data['resonatorParam']['pumpWatt']  # 入射功率
    eta_c = data['resonatorParam']['pumpEfficiency']  # 泵浦
    lm = data['modelAttributeList'][2]['length'] # 增益介质长度
    rm = data['modelAttributeList'][2]['radius']  # 增益介质半径
    U_gain1, U5 = process_main_cavity(U_M1pre,  matrix_all[1], aperture_all[0], aperture_all[1], aperture_all[2],lm,rm, P_in, lambda_, eta_c, r2, t2)
    # 第二阶段：自由腔传输
    # log_gpu_memory("222")
    U_gain2, U9,U2 = process_free_cavity(U_M2pre , matrix_all[1],matrix_all[0],aperture_all[1], aperture_all[2],aperture_all[3], r2, r3, t2)
    U5 = U5 + U9
    del U9
    U=U5
    # 第三阶段：增益介质与合并
    U_gain1= U_gain1 + U_gain2
    del U_gain2
    # log_gpu_memory("333")
    U_M1 = process_gain_and_merge(U_gain1 ,matrix_all[1], aperture_all[1], aperture_all[0], r1, lm,rm, P_in, lambda_, eta_c)
    del U_gain1
    # 显存清理
    # cp.get_default_memory_pool().free_all_blocks()
    return U_M1, U, U2
    
def process_main_cavity(U_M1pre, H_fsf, B_CatEye1, B_aper, B_CatEye2,lm,rm, P_in, lambda_, eta_c, r2, t2):
    U1 = main_cavity_trans(U_M1pre, H_fsf, B_CatEye1, B_aper, B_CatEye2, lm,rm,P_in, lambda_, eta_c)
    U = operator_reflectivity(U1, r2)
    U_gain1 = cal_field_transition(U, H_fsf, B_CatEye2, B_aper)
    del U
    U5 = operator_transmissivity(U1, t2)
    del U1
    cp.get_default_memory_pool().free_all_blocks()
    return U_gain1, U5  # 函数返回后 U1 的显存自动释放

def process_free_cavity(U_M2pre, H_fsf,H_fsdf,B_aper, B_CatEye2, B_CatEye3, r2, r3, t2):
    U2 = cal_field_transition(U_M2pre, H_fsdf, B_CatEye2, B_CatEye3)
    U8 = cal_field_transition(operator_reflectivity(U2, r3), H_fsdf, B_CatEye3, B_CatEye2)
    U_gain2 = cal_field_transition(operator_transmissivity(U8, t2) , H_fsf, B_CatEye2, B_aper)
    cp.get_default_memory_pool().free_all_blocks()
    # log_gpu_memory("After process_free_cavity")
    return U_gain2, operator_reflectivity(U8, r2) , U2  # U8 显存在子函数结束时释放

def process_gain_and_merge(U_gain1, H_fsf, B_aper, B_CatEye1, r1, lm,rm, P_in, lambda_, eta_c):
    U_combined = U_gain1
    U_combined = propagation_within_gain(U_combined, lm,rm, P_in, lambda_, eta_c)
    U = cal_field_transition(U_combined, H_fsf, B_aper, B_CatEye1)
    del U_combined
    U= operator_reflectivity(U, r1)
    cp.get_default_memory_pool().free_all_blocks()
    return U

def cal_final_output(matrix_all, aperture_all, data,user_id):
    # Iten_out: 输出平面上的光强分布，可以直接计算输出功率
    # t: 迭代终止条件
    # s_it1 和 s_it2 分别是迭代终止时 M1 和 M2 上的场分布
    #部分参数写死
    epsilon = 8.854187817e-12
    c0 = 3e8
    result={}
    logger.info("时间:%s", datetime.datetime.now())
    lambda_ = data['resonatorParam']['lambda']*1e-9
    U_M1pre = 1  # M1初始场分布
    U_M2pre = 0  # M2初始场分布
    r_max = max(item['radius'] for item in data['modelAttributeList'])
    # [tempU1, tempU2, _] = one_roundtrip_distribution(U_M1pre, U_M2pre, H_fsdf, H_fsf, B_aper, B_CatEye1, B_CatEye2,
    #                                                    B_CatEye3, r1, r2, r3, P_in, lambda_,eta_c)
    [tempU1, tempU2, _] = one_roundtrip_distribution(U_M1pre, U_M2pre, matrix_all,aperture_all,data,lambda_)
    t = 1
    delta,_=calculate_fft_parameters(r_max, sampling_num=data['fastFTParam']['sampleNumber'],
                                    window_expand_factor=data['fastFTParam']['windowExpandFactor'])
    c = float('inf')
    while c > 0.0001:
        [s_it1, s_it2, U2] = one_roundtrip_distribution(tempU1, tempU2, matrix_all,aperture_all,data,lambda_)
        
        a1 = cp.sum(cp.abs(cp.abs(s_it1) - cp.abs(tempU1)))
        b1 = cp.sum(cp.abs(tempU1))
        c1 = a1 / b1
        del a1, b1
        a2 = cp.sum(cp.abs(cp.abs(s_it2) - cp.abs(tempU2)))
        b2 = cp.sum(cp.abs(tempU2))
        c2 = a2 / b2
        del  a2, b2
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
        R = 1 - data['modelAttributeList'][7]['reflectivity'] ** 2
       
        Iten_out = R * 0.5 * (const.epsilon_0* const.c) * cp.abs(U) ** 2  # 电场的振幅分布转化为光强分布
        Pout = cp.sum(Iten_out).item()*delta**2  # 输出功率
        del U, U2, Iten_out 
        
        logger.info(f'迭代次数: {t} 传输系数main: {v1} 传输系数free: {v2} 输出功率: {Pout} 终止判定1: {c} 终止判定2: {c2}')
        # 用字典记录每次的数据
        result["iterationCount"] = t
        result["transmissionCoefficientMain"] = v1.item()
        result["transmissionCoefficientFree"] = v2.item()
        result["outputPower"] = Pout
        result["isEnd"]=False
        yield result
        # yield f'迭代次数: {t} 主共振腔传输系数: {v1} 自由空间腔传输系数: {v2} 输出光功率: {Pout * delta * delta}'
        t += 1
        # 终止条件
        if t > 1000:  # 改为10测试完整运行
            t=t-1
            break
        if data['resonatorParam']['pumpWatt'] < 1e-15:
            break
        if c > 0.0001:
            del s_it1, s_it2
            # 强制释放显存
            cp.get_default_memory_pool().free_all_blocks()

    logger.info("时间:%s", datetime.datetime.now())
    #部分参数写死
    U_M1, _, _ = one_roundtrip_distribution(s_it1, s_it2, matrix_all,aperture_all,data,lambda_)
    
    # V_round = cal_trans_factor(U_M1, s_it1)  # 一个 roundtrip 的传输系数
    del U_M1
   
    s_it1_buffer = io.BytesIO()
    sio.savemat( s_it1_buffer, {'matrix': s_it1.get()}, format='5',do_compression=True)
    del s_it1
    key1=user_id+uuid.uuid4().hex[:6]
    set_redis_data(key1, s_it1_buffer.getvalue())
    
    s_it2_buffer = io.BytesIO()
    sio.savemat( s_it2_buffer, {'matrix': s_it2.get()}, format='5',do_compression=True)
    del s_it2
    key2=user_id+uuid.uuid4().hex[:6]
    set_redis_data(key2, s_it2_buffer.getvalue())
    
    result={}
    result["iterationCount"] = t
    # data["fieldDistributionMain"] = s_it1_buffer.getvalue()
    result["fieldDistributionMain"] = key1
    # data["fieldDistributionFree"] = s_it2_buffer.getvalue()
    result['fieldDistributionFree'] = key2
    result["outputPower"] = Iten_out
    result["isEnd"]=True
    # return Iten_out, t, s_it1, s_it2, V_round
    return result