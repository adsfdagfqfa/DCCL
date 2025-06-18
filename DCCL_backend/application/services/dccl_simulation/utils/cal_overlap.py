import numpy as np
import cupy as cp

def cal_overlap(E1, E2, delta):
    E1 = E1 / cp.max(cp.abs(E1))  # 归一化
    E2 = E2 / cp.max(cp.abs(E2))
    over_temp = cp.sum(E1 * cp.conj(E2)) * (delta ** 2) # 计算两个归一化光场的重叠，通过将E1和E2的共轭相乘后求和，然后乘以delta的平方
    return over_temp
