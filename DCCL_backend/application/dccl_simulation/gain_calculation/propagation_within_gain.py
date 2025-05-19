import numpy as np

from .fun_of_gain import fun_of_gain
from application.utils.utility_function import log_gpu_memory

def propagation_within_gain(U_pre, lm, P_in, lambda_,eta_c):  # lm：增益介质的长度
    l = 0.001  # 分割粒度
    # U = U_pre.copy()  # 创建U_pre的副本以避免修改原始数组
    for i in range(int(np.ceil(lm / l))):  # 使用np.ceil确保循环次数足够
        g_ij = fun_of_gain(U_pre, l, P_in, lambda_,eta_c)
        U_pre *= g_ij
    return U_pre
