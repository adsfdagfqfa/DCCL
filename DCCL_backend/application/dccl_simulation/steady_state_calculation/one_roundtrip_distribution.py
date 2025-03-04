import numpy as np

from ..utils import cal_field_transition,operator_reflectivity,operator_transmissivity
from ..gain_calculation import propagation_within_gain
from .free_cavity_trans import free_cavity_trans
from .main_cavity_trans import main_cavity_trans



def one_roundtrip_distribution(U_M1pre, U_M2pre, H_fsdf, H_fsf, B_aper, B_CatEye1, B_CatEye2, B_CatEye3, r1, r2, r3,
                               P_in, lambda_):
    t2 = np.sqrt(1 - r2 ** 2)  # 透射光强率
    lm = 0.001
    U1 = main_cavity_trans(U_M1pre, H_fsf, B_CatEye1, B_aper, B_CatEye2, P_in, lambda_)
    U = operator_reflectivity(U1, r2)
    U_gain1 = cal_field_transition(U, H_fsf, B_CatEye2, B_aper)
    U5 = operator_transmissivity(U1, t2)
    U2 = free_cavity_trans(U_M2pre, H_fsdf, B_CatEye2, B_CatEye3)
    U = operator_reflectivity(U2, r3)
    U8 = free_cavity_trans(U, H_fsdf, B_CatEye3, B_CatEye2)
    U9 = operator_reflectivity(U8, r2)
    U = operator_transmissivity(U8, t2)
    U_gain2 = cal_field_transition(U, H_fsf, B_CatEye2, B_aper)
    U = U_gain1 + U_gain2
    U = propagation_within_gain(U, lm, P_in, lambda_)  # 所有光场在通过增益介质前应该被加在一起以一起放大
    U = cal_field_transition(U, H_fsf, B_aper, B_CatEye1)
    U_M1 = operator_reflectivity(U, r1)
    U_M2 = U5 + U9
    return U_M1, U_M2, U2
