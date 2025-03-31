import numpy as np
import cupy as cp
from ..utils.para_FFT import para_FFT


def aperture_gain(sigma, f, radius, r_CatEye):
    _, M, _, _, delta, _ = para_FFT(r_CatEye)
    m1, m2 = cp.meshgrid(cp.linspace(-M // 2, M // 2 - 1, M), cp.linspace(-M // 2, M // 2 - 1, M))
    T = cp.zeros((M, M))
    D = 2 * f * cp.tan(sigma)
    a = 0.5
    b = 0.5

    # 计算角锥棱镜对应圆面位置
    # i = np.where((m1 + a) ** 2 * delta ** 2 + (m2 + b) ** 2 * delta ** 2 <= radius ** 2)
    # T[i] = 1
    condition = ((m1 + a) ** 2 * delta ** 2 + (m2 + b) ** 2 * delta ** 2 <= radius ** 2)
    T[condition] = 1
    return T