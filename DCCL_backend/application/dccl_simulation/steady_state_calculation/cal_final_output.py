from cal_trans_factor import cal_trans_factor
from one_roundtrip_distribution import one_roundtrip_distribution
from steady_state import steady_state


def cal_final_output(H_fsdf, H_fsf, B_aper, B_CatEye1, B_CatEye2, B_CatEye3, r1, r2, r3, P_in, lambda_):
    # Iten_out: 输出平面上的光强分布，可以直接计算输出功率
    # t: 迭代终止条件
    # s_it1 和 s_it2 分别是迭代终止时 M1 和 M2 上的场分布
    Iten_out, t, s_it1, s_it2 = steady_state(H_fsdf, H_fsf, B_aper, B_CatEye1, B_CatEye2, B_CatEye3, r1, r2,
                                                      r3, P_in, lambda_)

    U_M1, _, _ = one_roundtrip_distribution(s_it1, s_it2, H_fsdf, H_fsf, B_aper, B_CatEye1, B_CatEye2, B_CatEye3, r1, r2,
                                         r3, P_in, lambda_)
    V_round = cal_trans_factor(U_M1, s_it1)  # 一个 roundtrip 的传输系数

    return Iten_out, t, s_it1, s_it2, V_round