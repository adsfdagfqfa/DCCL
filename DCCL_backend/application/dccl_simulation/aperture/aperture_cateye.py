import numpy as np
from numpy import tan, linspace, meshgrid

from ..utils.para_FFT import para_FFT


def aperture_cateye(sigma, f, radius, r_MAX):
    _, M, _, _, delta, _ = para_FFT(r_MAX)  # 获取FFT参数
    m1, m2 = meshgrid(np.linspace(-M//2, M//2 - 1, M), np.linspace(-M // 2, M // 2 - 1, M))  # 生成采样点下标
    # T = np.zeros((M, M))  # 初始化边界函数矩阵
    T = np.zeros((M, M))
    a = 0.5  # 圆面对应圆心坐标
    b = 0.5
    D = 2 * f * tan(sigma)  # 计算D
    B = radius**2  # 计算B

    # 计算满足条件的索引并设置T的相应位置为1
    i = np.where((((m1 + a) * delta) ** 2 + ((m2 + b) * delta) ** 2 <= B) &
               (((m1 + a) * delta) ** 2 + ((m2 + b) * delta - D) ** 2 <= B))
    T[i] = 1

    return T
