# from scipy.fft import fft2, ifft2, fftshift, ifftshift
import cupyx.scipy.fft as cufft
import cupy as cp
import scipy.fft




def cal_field_transition(U_pre, H, B_aper, B_lens):
    # # 原始光场的FFT变换
    # B = fftshift(fft2(ifftshift(U_pre * B_aper)))
    # # 到达面光场
    # U = fftshift(ifft2(ifftshift(H * B))) * B_lens
    scipy.fft.set_global_backend(cufft)
    B = cufft.fftshift(cufft.fft2(cufft.ifftshift(U_pre * B_aper)))
    U = cufft.fftshift(cufft.ifft2(cufft.ifftshift(H * B))) * B_lens
    return U
