import numpy as np
import cupy as cp
from .utils import calculate_fft_parameters
def cal_transfer_matrix(length, lambda_, M, deltaF):
    # _, M, W, _, _, deltaF = para_FFT(r_max)  # 获取FFT参数
    k = 2 * cp.pi / lambda_  # 计算波数
    n1, n2 = cp.meshgrid(cp.linspace(-M//2, M//2 - 1, M), cp.linspace(-M//2, M//2 - 1, M))  # 生成采样点下标
    H = cp.exp(1j * k * length * cp.sqrt(1 - (lambda_ * n1 * deltaF)**2 - (lambda_ * n2 * deltaF)**2))  # 计算传递函数矩阵

    return H

def cal_all_matrix(data,r_max,angle_1,angle_2):
    matrix_all=[]
    #这里需要分为两个传输矩阵分别计算，差不多相当于写死,angle_1与angle_2分别是谐振腔与自由空间传输腔内部稳定光束与主光轴的夹角
    d=data['distance'][5]/np.cos(angle_2)
    f=data['modelAttributeList'][1]['focalLength']/np.cos(angle_1)
    lambda_=data['resonatorParam']['lambda']*1e-9
    sampling_num = data['fastFTParam']['sampleNumber']
    window_expand_factor = data['fastFTParam']['windowExpandFactor']
    _,deltaF=calculate_fft_parameters(radius=r_max, sampling_num=sampling_num, window_expand_factor=window_expand_factor)
    H_fsdf = cal_transfer_matrix(d, lambda_,sampling_num, deltaF)
    H_fsf = cal_transfer_matrix(f, lambda_,sampling_num, deltaF)
    #complex64为单精度复数,保留数据中的虚部与实部
    matrix_all.append(H_fsdf.astype(cp.complex64))
    matrix_all.append(H_fsf.astype(cp.complex64)) 
    return matrix_all