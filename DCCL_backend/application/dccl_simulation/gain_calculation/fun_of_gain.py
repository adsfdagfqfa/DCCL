import numpy as np
import cupy as cp
from scipy.special import lambertw
import time
import datetime


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
    A = cp.zeros(I.shape, dtype=cp.float32)
    # A = np.zeros_like(I, dtype=np.float32)
    B = A.copy()
    A[m] = V_sat2 / I[m]
    B[m] = cp.log(I[m])
    c1 = B + I / V_sat2

    B = 1 / V_sat2 * cp.exp(g0 * lm + c1)
    # B = lambertw(B)
    # print("2:", datetime.datetime.now())
    # 主要的耗时位置
    
    B_cpu = cp.asnumpy(B)  # 将CuPy数组转换为NumPy数组
    B_lambertw = lambertw(B_cpu)  # 使用SciPy的lambertw函数
    B = cp.asarray(B_lambertw, dtype=cp.complex64)  # 将结果转换回CuPy数组

    # print("2:", datetime.datetime.now())
    C = A * B
    g_ij = cp.sqrt(C)

    return g_ij
