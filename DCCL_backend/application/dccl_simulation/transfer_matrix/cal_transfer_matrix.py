from numpy import pi, linspace, meshgrid, exp, sqrt

from ..utils import para_FFT


def cal_transfer_matrix(length, lambda_, r_max):
    _, M, W, _, _, deltaF = para_FFT(r_max)  # 获取FFT参数
    k = 2 * pi / lambda_  # 计算波数
    n1, n2 = meshgrid(linspace(-M//2, M//2 - 1, M), linspace(-M//2, M//2 - 1, M))  # 生成采样点下标
    H = exp(1j * k * length * sqrt(1 - (lambda_ * n1 * deltaF)**2 - (lambda_ * n2 * deltaF)**2))  # 计算传递函数矩阵

    return H