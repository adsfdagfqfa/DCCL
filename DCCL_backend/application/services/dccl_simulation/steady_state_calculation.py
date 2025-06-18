
def free_cavity_trans(U_pre, H_fsdf, B_CatEye2, B_CatEye3):
    U = cal_field_transition(U_pre, H_fsdf, B_CatEye2, B_CatEye3)  # M2-L3入射表面
    return U

def main_cavity_trans(U_pre, H_fsf, B_CatEye1, B_aper, B_CatEye2, P_in, lambda_,eta_c):
    lm = 0.001  # 增益介质长度
    U = cal_field_transition(U_pre, H_fsf, B_CatEye1, B_aper)  # M1-L1入射表面
    U = propagation_within_gain(U, lm, P_in, lambda_,eta_c)
    U = cal_field_transition(U, H_fsf, B_aper, B_CatEye2)  # L2出射表面-M2
    return U

def one_roundtrip_distribution(U_M1pre, U_M2pre, H_fsdf, H_fsf, B_aper, B_CatEye1, B_CatEye2, B_CatEye3, r1, r2, r3,
                               P_in, lambda_,eta_c):
    t2 = cp.sqrt(1 - r2 ** 2)  # 透射光强率
    lm = 0.001

    # U1 = main_cavity_trans(U_M1pre, H_fsf, B_CatEye1, B_aper, B_CatEye2, P_in, lambda_,eta_c)
    # U = operator_reflectivity(U1, r2)
    

    # U_gain1 = cal_field_transition(U, H_fsf, B_CatEye2, B_aper)
    # U5 = operator_transmissivity(U1, t2)
    # del U1

    # U2 = free_cavity_trans(U_M2pre, H_fsdf, B_CatEye2, B_CatEye3)
    # U = operator_reflectivity(U2, r3)
  

    # U8 = free_cavity_trans(U, H_fsdf, B_CatEye3, B_CatEye2)
    # U9 = operator_reflectivity(U8, r2)
    # U = operator_transmissivity(U8, t2)
    # del U8

    # U_gain2 = cal_field_transition(U, H_fsf, B_CatEye2, B_aper)
    # U = U_gain1 + U_gain2
    # del U_gain1
    # del U_gain2
    
    # U = propagation_within_gain(U, lm, P_in, lambda_,eta_c)  # 所有光场在通过增益介质前应该被加在一起以一起放大

    # U = cal_field_transition(U, H_fsf, B_aper, B_CatEye1)
    # U_M1 = operator_reflectivity(U, r1)
    # U_M2 = U5 + U9
    # del U5
    # del U9
    # del U
    # # 强制释放显存
    # cp.get_default_memory_pool().free_all_blocks()
    # log_gpu_memory("111")
    U_gain1, U5 = process_main_cavity(U_M1pre, H_fsf, B_CatEye1, B_aper, B_CatEye2, P_in, lambda_, eta_c, r2, t2)
    # 第二阶段：自由腔传输
    # log_gpu_memory("222")
    U_gain2, U9,U2 = process_free_cavity(U_M2pre , H_fsf, H_fsdf,B_aper, B_CatEye2, B_CatEye3, r2, r3, t2)
    U5 = U5 + U9
    del U9
    U=U5
    # 第三阶段：增益介质与合并
    U_gain1= U_gain1 + U_gain2
    del U_gain2
    # log_gpu_memory("333")
    U_M1 = process_gain_and_merge(U_gain1 ,H_fsf, B_aper, B_CatEye1, r1, lm, P_in, lambda_, eta_c)
    del U_gain1
    # 显存清理
    # cp.get_default_memory_pool().free_all_blocks()
    return U_M1, U, U2
    
def process_main_cavity(U_M1pre, H_fsf, B_CatEye1, B_aper, B_CatEye2, P_in, lambda_, eta_c, r2, t2):
    U1 = main_cavity_trans(U_M1pre, H_fsf, B_CatEye1, B_aper, B_CatEye2, P_in, lambda_, eta_c)
    U = operator_reflectivity(U1, r2)
    U_gain1 = cal_field_transition(U, H_fsf, B_CatEye2, B_aper)
    U5 = operator_transmissivity(U1, t2)
    del U1,U
    cp.get_default_memory_pool().free_all_blocks()
    return U_gain1, U5  # 函数返回后 U1 的显存自动释放

def process_free_cavity(U_M2pre, H_fsf,H_fsdf,B_aper, B_CatEye2, B_CatEye3, r2, r3, t2):
    
    U2 = cal_field_transition(U_M2pre, H_fsdf, B_CatEye2, B_CatEye3)
    U8 = cal_field_transition(operator_reflectivity(U2, r3), H_fsdf, B_CatEye3, B_CatEye2)
    U_gain2 = cal_field_transition(operator_transmissivity(U8, t2) , H_fsf, B_CatEye2, B_aper)
    cp.get_default_memory_pool().free_all_blocks()
    # log_gpu_memory("After process_free_cavity")
    return U_gain2, operator_reflectivity(U8, r2) , U2  # U8 显存在子函数结束时释放

def process_gain_and_merge(U_gain1, H_fsf, B_aper, B_CatEye1, r1, lm, P_in, lambda_, eta_c):
    
    U_combined = U_gain1
   
    U_combined = propagation_within_gain(U_combined, lm, P_in, lambda_, eta_c)
    
    U = cal_field_transition(U_combined, H_fsf, B_aper, B_CatEye1)
    del U_combined
    U= operator_reflectivity(U, r1)
    cp.get_default_memory_pool().free_all_blocks()
    return U

def steady_state(H_fsdf, H_fsf, B_aper, B_CatEye1, B_CatEye2, B_CatEye3, r1, r2, r3, P_in, lambda_,eta_c):
    # 开始计时
    start_time = time.time()
    # 经过的时间
    elapsed_time = 0
    U_M1pre = 1  # M1初始场分布
    U_M2pre = 0  # M2初始场分布
    [tempU1, tempU2, _] = one_roundtrip_distribution(U_M1pre, U_M2pre, H_fsdf, H_fsf, B_aper, B_CatEye1, B_CatEye2,
                                                       B_CatEye3, r1, r2, r3, P_in, lambda_,eta_c)
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
        
        
        
        logger.info(f'迭代次数: {t} 传输系数main: {v1} 传输系数free: {v2} 输出功率: {Pout * delta * delta} 终止判定1: {c} 终止判定2: {c2}')
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
        if t > 1000:  # 改为10测试完整运行
            break
        if P_in < 1e-15:
            break
        if c > 0.0001:
            del s_it1, s_it2
            # 强制释放显存
            cp.get_default_memory_pool().free_all_blocks()
    return Pout.item() *delta*delta, t-1, s_it1, s_it2  # 迭代终止时M1和M2上的场分布