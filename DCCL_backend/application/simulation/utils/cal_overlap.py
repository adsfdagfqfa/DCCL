import numpy as np


def cal_overlap(E1, E2, delta):
    E1 = E1 / np.max(np.abs(E1))  # 归一化
    E2 = E2 / np.max(np.abs(E2))
    over_temp = np.sum(E1 * np.conj(E2)) * (delta ** 2) # 计算两个归一化光场的重叠，通过将E1和E2的共轭相乘后求和，然后乘以delta的平方
    return over_temp
