import numpy as np
from ..utils.para_FFT import para_FFT


def aperture_gain(sigma, f, radius, r_CatEye):
    _, M, _, _, delta, _ = para_FFT(r_CatEye)
    m1, m2 = np.meshgrid(np.linspace(-M // 2, M // 2 - 1, M), np.linspace(-M // 2, M // 2 - 1, M))
    T = np.zeros((M, M))
    D = 2 * f * np.tan(sigma)
    a = 0.5
    b = 0.5

    # 计算角锥棱镜对应圆面位置
    i = np.where((m1 + a) ** 2 * delta ** 2 + (m2 + b) ** 2 * delta ** 2 <= radius ** 2)
    T[i] = 1

    return T