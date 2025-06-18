import numpy as np
import cupy as cp
# from scipy.special import lambertw
import time
import datetime 
from cupyx.scipy.special import lambertw as cupyx_lambertw
from application.utils.utility_function import log_gpu_memory
def propagation_within_gain(U_pre, lm, P_in, lambda_,eta_c):  # lm：增益介质的长度
    l = 0.001  # 分割粒度
    # U = U_pre.copy()  # 创建U_pre的副本以避免修改原始数组
    for i in range(int(np.ceil(lm / l))):  # 使用np.ceil确保循环次数足够
        g_ij = fun_of_gain(U_pre, l, P_in, lambda_,eta_c)
        U_pre *= g_ij
    return U_pre


def fun_of_gain(in_U, lm, P_in, lambda_,eta_c):
    #eta_c泵浦效率
    # 开始计时
    start_time = time.time()
    # 常数
    c = 3e8
    h = 6.626e-34
    epsilon = 8.854187817e-12
    mu0 = 4 * cp.pi * 1e-7

    # 系统参数,这里分别是sigma吸收/发射截面，tau_f上能级(激发态)粒子寿命
    sigma = 15.6e-23  # Nd:YVO4
    tau_f = 100e-6  # Nd:YVO4
    #频率
    nu = c / lambda_

    # eta_Q = 0.95
    # eta_S = 0.76
    # eta_B = 0.90
    # eta_P = 0.75
    # eta_T = 0.99
    # eta_a = 0.91
    # eta_c = eta_Q * eta_S * eta_B * eta_P * eta_T * eta_a  # 从泵浦到存储功率的效率，不包括重叠效率 eta_B
    # eta_c类似泵浦效率
    #eta_c = 0.72
    a_m = 0.003  # 泵浦光束半径
    V = cp.pi * a_m ** 2 * lm
    # deltaT = 0.3e-6 / 200
    # tau = 0.3e-6

    I_s = h * nu / (sigma * tau_f) #增益介质饱和强度
    V_sat2 = I_s / (0.5 * (epsilon * c))
    g0 = eta_c * P_in / (I_s * V)

    # 计算强度

    I = 2 * cp.abs(in_U) ** 2

    # I = cp.asarray(I, dtype=cp.float32)
    # 创建对应的bool掩码
    m = I != 0
    # A = cp.zeros(I.shape, dtype=cp.float32)
    # # A = np.zeros_like(I, dtype=np.float32)
    # B = A.copy()
    # A[m] = V_sat2 / I[m]
    # B[m] = cp.log(I[m])

    A = cp.where(m, V_sat2 / I, 0.0)
    B = cp.where(m, cp.log(I), 0.0)
    c1 = B + I / V_sat2
    del I, B, m
    # B = 1 / V_sat2 * cp.exp(g0 * lm + c1)
    B_new = cp.exp(g0 * lm + c1)
    del c1
    # log_gpu_memory("fun_of_gain4")
    B_new *= cp.reciprocal(V_sat2)
    # 主要的耗时位置
    
    # B_cpu = cp.asnumpy(B)  # 将CuPy数组转换为NumPy数组
    # B_lambertw = lambertw(B_cpu)  # 使用SciPy的lambertw函数
    # B = cp.asarray(B_lambertw, dtype=cp.complex64)  # 将结果转换回CuPy数组
    #使用cupy仓库的14.0版本，含有GPU加速的lambertw函数
    # B=cupyx_lambertw(B)
    B_new = cupyx_lambertw(B_new)
    # log_gpu_memory("fun_of_gain6")
    cp.multiply(A, B_new, out=B_new)
    del A
    cp.sqrt(B_new,out=B_new)
    # log_gpu_memory("fun_of_gain7")
    return B_new
