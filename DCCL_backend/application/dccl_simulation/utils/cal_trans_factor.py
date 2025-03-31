import numpy as np
import cupy as cp

def cal_trans_factor(U1, U2):
    U3 = cp.abs(U1) ** 2
    U4 = cp.abs(U2) ** 2
    V = cp.sum(U3) / cp.sum(U4)
    return V
