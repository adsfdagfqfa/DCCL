from ..utils import cal_field_transition


def free_cavity_trans(U_pre, H_fsdf, B_CatEye2, B_CatEye3):
    U = cal_field_transition(U_pre, H_fsdf, B_CatEye2, B_CatEye3)  # M2-L3入射表面
    return U