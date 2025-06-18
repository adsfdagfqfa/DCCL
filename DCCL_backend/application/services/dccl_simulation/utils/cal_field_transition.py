# from scipy.fft import fft2, ifft2, fftshift, ifftshift
import cupyx.scipy.fft as cufft
import cupy as cp
import scipy.fft

from cupyx.scipy.sparse import csr_matrix

from application.utils.utility_function import log_gpu_memory

def cal_field_transition(U_pre, H, B_aper, B_lens):
  
    # # 原始光场的FFT变换
    # B = fftshift(fft2(ifftshift(U_pre * B_aper)))
    # # 到达面光场
    # U = fftshift(ifft2(ifftshift(H * B))) * B_lens
    #scipy.fft.set_global_backend(cufft)
    # B = cufft.fftshift(cufft.fft2(cufft.ifftshift(U_pre * B_aper)))
    # U = cufft.fftshift(cufft.ifft2(cufft.ifftshift(H * B))) * B_lens

    U=cufft.fftshift(cufft.ifft2(cufft.ifftshift(H * cufft.fftshift(cufft.fft2(cufft.ifftshift(U_pre * B_aper)))))) * B_lens
    # cp.get_default_memory_pool().free_all_blocks() 
    # temp = U_pre * B_aper
    # temp = cufft.ifftshift(temp)
    # temp = cufft.fft2(temp)
    # temp = cufft.fftshift(temp)
    # temp *= H  # 原地乘法，减少显存分配
    # temp = cufft.ifftshift(temp)
    # temp = cufft.ifft2(temp)
    # temp = cufft.fftshift(temp)
    # U = temp * B_lens
    # cp.get_default_memory_pool().free_all_blocks()  # 确保所有GPU操作完成
    # log_gpu_memory("cal_field_transition")
    return U
