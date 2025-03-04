
import numpy as np
import cupy as cp
from .cal_transfer_matrix import cal_transfer_matrix
def cal_all_matrix(data,r_max,angle_1,angle_2):
    matrix_all=[]
    #这里需要分为两个传输矩阵分别计算，差不多相当于写死,angle_1与angle_2分别是谐振腔与自由空间传输腔内部稳定光束与主光轴的夹角
    d=data['distance'][5]/np.cos(angle_2)
    f=data['modelAttributeList'][1]['focalLength']/np.cos(angle_1)
    H_fsdf = cal_transfer_matrix(d, data['resonatorParam']['lambda'], r_max)
    H_fsf = cal_transfer_matrix(f, data['resonatorParam']['lambda'], r_max)
    matrix_all.append(cp.asarray(H_fsdf, dtype=cp.complex64))
    matrix_all.append(cp.asarray(H_fsf, dtype=cp.complex64))    
    return matrix_all