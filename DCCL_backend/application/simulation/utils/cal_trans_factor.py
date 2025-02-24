import numpy as np


def cal_trans_factor(U1, U2):
    U3 = np.abs(U1) ** 2
    U4 = np.abs(U2) ** 2
    V = np.sum(U3) / np.sum(U4)
    return V
