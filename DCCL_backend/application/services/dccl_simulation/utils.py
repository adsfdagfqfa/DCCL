import cupyx.scipy.fft as cufft
import cupy as cp
import scipy.fft
# 利用传输矩阵H来计算光场传播
def cal_field_transition(U_pre, H, B_aper, B_lens):
  
    # # 原始光场的FFT变换
    # B = fftshift(fft2(ifftshift(U_pre * B_aper)))
    # # 到达面光场
    # U = fftshift(ifft2(ifftshift(H * B))) * B_lens
    #scipy.fft.set_global_backend(cufft)
    B = cufft.fftshift(cufft.fft2(cufft.ifftshift(U_pre * B_aper)))
    U = cufft.fftshift(cufft.ifft2(cufft.ifftshift(H * B))) * B_lens
    return U

def cal_overlap(E1, E2, delta):
    E1 = E1 / cp.max(cp.abs(E1))  # 归一化
    E2 = E2 / cp.max(cp.abs(E2))
    over_temp = cp.sum(E1 * cp.conj(E2)) * (delta ** 2) # 计算两个归一化光场的重叠，通过将E1和E2的共轭相乘后求和，然后乘以delta的平方
    return over_temp
# 计算传输因子
def cal_trans_factor(U1, U2):
    U3 = cp.abs(U1) ** 2
    U4 = cp.abs(U2) ** 2
    V = cp.sum(U3) / cp.sum(U4)
    return V
# 计算光场反射
def operator_reflectivity(U_pre, r):
    U = U_pre *( r * 1j )  # 在Python中，虚数单位是1j
    return U

# 计算光场透射
def operator_transmissivity(U_pre, t):
    U = U_pre * t  # 在Python中，乘法操作直接使用*
    return U

# 返回相关参数
def calculate_fft_parameters(radius, itr=300, sampling_num=8192, window_expand_factor=3):
    """
    计算空间频率与采样间隔参数。

    :param radius: 入射面半径
    :param itr: 迭代次数，默认 300
    :param sampling_num: 采样点数量，默认 8192
    :param window_expand_factor: 计算窗口扩展因子，默认 3
    :return: delta, delta_f
    :raises ValueError: 如果输入参数不符合要求
    """
    if radius <= 0:
        raise ValueError("radius must be positive.")
    if sampling_num <= 0:
        raise ValueError("sampling_num must be positive.")
    if window_expand_factor <= 0:
        raise ValueError("window_expand_factor must be positive.")

    window_size = 2 * window_expand_factor * radius  # 计算窗口尺寸 2Gr
    delta = window_size / sampling_num               # 空域采样间隔
    delta_f = 1.0 / window_size                      # 频域采样间隔

    return delta,delta_f