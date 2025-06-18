from numpy import pi, linspace, meshgrid, exp, sqrt
import cupy as cp
from ..utils import para_FFT


def cal_transfer_matrix(length, lambda_, r_max):
    _, M, W, _, _, deltaF = para_FFT(r_max)  # 获取FFT参数
    k = 2 * cp.pi / lambda_  # 计算波数
    n1, n2 = cp.meshgrid(cp.linspace(-M//2, M//2 - 1, M), cp.linspace(-M//2, M//2 - 1, M))  # 生成采样点下标
    H = cp.exp(1j * k * length * cp.sqrt(1 - (lambda_ * n1 * deltaF)**2 - (lambda_ * n2 * deltaF)**2))  # 计算传递函数矩阵

    return H