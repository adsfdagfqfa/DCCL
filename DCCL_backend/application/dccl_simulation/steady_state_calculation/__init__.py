import types
from ..utils import cal_trans_factor
from .one_roundtrip_distribution import one_roundtrip_distribution
from .steady_state import steady_state


def cal_final_output(matrix_all, aperture_all, data):
    # Iten_out: 输出平面上的光强分布，可以直接计算输出功率
    # t: 迭代终止条件
    # s_it1 和 s_it2 分别是迭代终止时 M1 和 M2 上的场分布
    #部分参数写死
    generator = steady_state(matrix_all[0], matrix_all[1], aperture_all[1], aperture_all[0], aperture_all[2]*aperture_all[3],
                                            aperture_all[4], data['modelAttributeList'][0]['reflectivity'],
                                            data['modelAttributeList'][4]['reflectivity'],data['modelAttributeList'][7]['reflectivity'],
                                            data['resonatorParam']['pumpWatt'],data['resonatorParam']['lambda'] )
    # Iten_out, t, s_it1, s_it2 = steady_state(H_fsdf, H_fsf, B_aper, B_CatEye1, B_CatEye2, B_CatEye3, r1, r2,
    #                                                   r3, P_in, lambda_)

    try:
        while True:
            value = next(generator)
            yield value
    except StopIteration as e:
        # 捕获steay_state最终返回值
        Iten_out, t, s_it1, s_it2 = e.value

    #部分参数写死
    U_M1, _, _ = one_roundtrip_distribution(s_it1, s_it2, matrix_all[0], matrix_all[1], aperture_all[1], aperture_all[0], 
                                            aperture_all[2]*aperture_all[3],
                                            aperture_all[4], data['modelAttributeList'][0]['reflectivity'],
                                            data['modelAttributeList'][4]['reflectivity'],data['modelAttributeList'][7]['reflectivity'],
                                            data['resonatorParam']['pumpWatt'],data['resonatorParam']['lambda'] )
    # U_M1, _, _ = one_roundtrip_distribution(s_it1, s_it2, H_fsdf, H_fsf, B_aper, B_CatEye1, B_CatEye2, B_CatEye3, r1, r2,
    #                                      r3, P_in, lambda_)
    V_round = cal_trans_factor(U_M1, s_it1)  # 一个 roundtrip 的传输系数

    return Iten_out, t, s_it1, s_it2, V_round