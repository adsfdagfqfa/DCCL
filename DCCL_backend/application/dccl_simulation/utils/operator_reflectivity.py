from application.utils.utility_function import log_gpu_memory   

def operator_reflectivity(U_pre, r):
    U = U_pre *( r * 1j )  # 在Python中，虚数单位是1j
    return U