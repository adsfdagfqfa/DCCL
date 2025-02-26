from cal_field_transition import cal_field_transition
from propagation_within_gain import propagation_within_gain


def main_cavity_trans(U_pre, H_fsf, B_CatEye1, B_aper, B_CatEye2, P_in, lambda_):
    lm = 0.001  # 增益介质长度
    U = cal_field_transition(U_pre, H_fsf, B_CatEye1, B_aper)  # M1-L1入射表面
    U = propagation_within_gain(U, lm, P_in, lambda_)
    U = cal_field_transition(U, H_fsf, B_aper, B_CatEye2)  # L2出射表面-M2
    return U