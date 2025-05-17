# from scipy.fft import fft2, ifft2, fftshift, ifftshift
import cupyx.scipy.fft as cufft
import cupy as cp
import scipy.fft

from cupyx.scipy.sparse import csr_matrix



def cal_field_transition(U_pre, H, B_aper, B_lens):
    # if isinstance(U_pre, csr_matrix):
    #     print("U_pre 是 CSR 格式的稀疏矩阵")
    # else:
    #     print("U_pre 不是 CSR 格式的稀疏矩阵")

    # # 原始光场的FFT变换
    # B = fftshift(fft2(ifftshift(U_pre * B_aper)))
    # # 到达面光场
    # U = fftshift(ifft2(ifftshift(H * B))) * B_lens
    #scipy.fft.set_global_backend(cufft)
    B_aper_dense = B_aper.toarray()#转为密集型矩阵
    B_lens_dense = B_lens.toarray()
    B = cufft.fftshift(cufft.fft2(cufft.ifftshift(U_pre * B_aper_dense)))
    U = cufft.fftshift(cufft.ifft2(cufft.ifftshift(H * B))) * B_lens_dense
    del B_aper_dense
    del B_lens_dense
    cp.get_default_memory_pool().free_all_blocks()  
    return U
