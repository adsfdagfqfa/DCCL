import types,io,scipy as sio
import uuid
from ..utils import cal_trans_factor
from .one_roundtrip_distribution import one_roundtrip_distribution
from .steady_state import steady_state
import cupyx.scipy.sparse as cp_sparse
from flask import g
from scipy.sparse import csr_matrix
from application.utils.utility_function import csr_matrix_to_dict
from application.utils.redis_utils import set_redis_data
def cal_final_output(matrix_all, aperture_all, data):
    # Iten_out: 输出平面上的光强分布，可以直接计算输出功率
    # t: 迭代终止条件
    # s_it1 和 s_it2 分别是迭代终止时 M1 和 M2 上的场分布
    #部分参数写死
    lambda_ = data['resonatorParam']['lambda']*1e-9
    generator = steady_state(matrix_all[0], matrix_all[1], aperture_all[1], aperture_all[0], aperture_all[2]*aperture_all[3],
                                            aperture_all[4], data['modelAttributeList'][0]['reflectivity'],
                                            data['modelAttributeList'][4]['reflectivity'],data['modelAttributeList'][7]['reflectivity'],
                                            data['resonatorParam']['pumpWatt'],lambda_,
                                            data['resonatorParam']['pumpEfficiency'])
    # Iten_out, t, s_it1, s_it2 = steady_state(H_fsdf, H_fsf, B_aper, B_CatEye1, B_CatEye2, B_CatEye3, r1, r2,
    #                                                   r3, P_in, lambda_)

    try:
        while True:
            value = next(generator)
            # 这里的value是一个字典，包含了迭代次数、传输系数和输出功率，用来记录每次迭代的数据
            # 这里可以将value的内容打印出来，或者存储到一个列表中
            yield value
    except StopIteration as e:
        # 捕获steay_state最终返回值
        Iten_out, t, s_it1, s_it2 = e.value

    #部分参数写死
    U_M1, _, _ = one_roundtrip_distribution(s_it1, s_it2, matrix_all[0], matrix_all[1], aperture_all[1], aperture_all[0], 
                                            aperture_all[2]*aperture_all[3],
                                            aperture_all[4], data['modelAttributeList'][0]['reflectivity'],
                                            data['modelAttributeList'][4]['reflectivity'],data['modelAttributeList'][7]['reflectivity'],
                                            data['resonatorParam']['pumpWatt'],lambda_ ,
                                            data['resonatorParam']['pumpEfficiency'])
    # U_M1, _, _ = one_roundtrip_distribution(s_it1, s_it2, H_fsdf, H_fsf, B_aper, B_CatEye1, B_CatEye2, B_CatEye3, r1, r2,
    #                                      r3, P_in, lambda_)
    V_round = cal_trans_factor(U_M1, s_it1)  # 一个 roundtrip 的传输系数

    #将s_it1和s_it2用稀疏矩阵的格式储存
    # s_it1_csr = cp_sparse.csr_matrix(s_it1)
    # s_it2_csr = cp_sparse.csr_matrix(s_it2)
    # s_it1_cpu = csr_matrix(s_it1_csr.get())
    # s_it2_cpu = csr_matrix(s_it2_csr.get())

    #使用mat格式来储存s_it1和s_it2,相比于直接储存csr_matrix格式，mat格式不用额外处理
    s_it1_buffer = io.BytesIO()
    sio.savemat( s_it1_buffer, {'matrix': s_it1}, format='5',docompress=True)
    key1=g.user_id+uuid.uuid4().hex[:6]
    set_redis_data(key1, s_it1_buffer.getvalue())
    
    s_it2_buffer = io.BytesIO()
    sio.savemat( s_it2_buffer, {'matrix': s_it2}, format='5',docompress=True)
    key2=g.user_id+uuid.uuid4().hex[:6]
    set_redis_data(key2, s_it2_buffer.getvalue())
    
    data={}
    data["iterationCount"] = t
    # data["fieldDistributionMain"] = s_it1_buffer.getvalue()
    data["fieldDistributionMain"] = key1
    # data["fieldDistributionFree"] = s_it2_buffer.getvalue()
    data['fieldDistributionFree'] = key2
    data["outputPower"] = Iten_out

    # return Iten_out, t, s_it1, s_it2, V_round
    return data