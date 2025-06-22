import numpy as np
import cupy as cp
from .utils import calculate_fft_parameters
# from cupyx.scipy.sparse import coo_matrix

def aperture_cateye(sigma, f, radius, M, delta):
    # _, M, _, _, delta, _ = para_FFT(r_MAX)  # 获取FFT参数
    m1, m2 = cp.meshgrid(cp.linspace(-M//2, M//2 - 1, M), cp.linspace(-M // 2, M // 2 - 1, M))  # 生成采样点下标
    # T = np.zeros((M, M))  # 初始化边界函数矩阵
    T = cp.zeros((M, M))
    a = 0.5  # 圆面对应圆心坐标
    b = 0.5
    D = 2 * f * cp.tan(sigma)  # 计算D
    B = radius**2  # 计算B

    # 计算满足条件的索引并设置T的相应位置为1
    # i = np.where((((m1 + a) * delta) ** 2 + ((m2 + b) * delta) ** 2 <= B) &
    #            (((m1 + a) * delta) ** 2 + ((m2 + b) * delta - D) ** 2 <= B))
    condition = (((m1 + a) * delta) ** 2 + ((m2 + b) * delta) ** 2 <= B) &\
    (((m1 + a) * delta) ** 2 + ((m2 + b) * delta - D) ** 2 <= B)
    T[condition] = 1
    return T
    # 获取非零元素的行列索引
    # rows, cols = cp.where(condition)

    # data = cp.ones(rows.size, dtype=cp.float32) 
    # coo_T = coo_matrix(
    #     (data, (rows, cols)),  # 注意参数格式：(data, (rows, cols))
    #     shape=(M, M)
    # )
    # csr_T = coo_T.tocsr()
    # return csr_T

def aperture_gain(sigma, f, radius,M,delta):
    # _, M, _, _, delta, _ = para_FFT(r_CatEye)
    m1, m2 = cp.meshgrid(cp.linspace(-M // 2, M // 2 - 1, M), cp.linspace(-M // 2, M // 2 - 1, M))
    T = cp.zeros((M, M))
    D = 2 * f * cp.tan(sigma)
    a = 0.5
    b = 0.5

    # 计算角锥棱镜对应圆面位置
    # i = np.where((m1 + a) ** 2 * delta ** 2 + (m2 + b) ** 2 * delta ** 2 <= radius ** 2)
    # T[i] = 1
    condition = ((m1 + a) ** 2 * delta ** 2 + ((m2 + b)  * delta-D/2 )** 2 <= radius ** 2)
    T[condition] = 1
    return T
    # rows, cols = cp.where(condition)
    # data = cp.ones(rows.size, dtype=cp.float32) 
    # coo_T = coo_matrix(
    #     (data, (rows, cols)),  # 注意参数格式：(data, (rows, cols))
    #     shape=(M, M)
    # )
    # csr_T = coo_T.tocsr()
    # return csr_T


def cal_all_aperture(data,r_max,angle_1,angle_2):

    aperture_all=[]
    sampling_num = data['fastFTParam']['sampleNumber']
    window_expand_factor = data['fastFTParam']['windowExpandFactor']
    delta,_=calculate_fft_parameters(radius=r_max, sampling_num=sampling_num, window_expand_factor=window_expand_factor)
    # for (index,item) in data['modelAttributeList']:
    for index, item in enumerate(data['modelAttributeList']):
        angle = angle_1 if index<=4 else angle_2
        #判断是镜子还是介质
        if item['type']=='lens' :
            aperture=aperture_cateye(angle,item['focalLength'],item['radius'],sampling_num,delta)
            #写死，如果是第五个元素（lens3），则将其孔径与第二个镜子的孔径相乘
            if index==5:
               aperture_all[2]=aperture_all[2]*aperture
               continue
            #计算的结果都放入GPU中去储存
            aperture_all.append(aperture.astype(cp.float32))

        elif item['type']=='medium':
            #这里同样写死第二个参数，由于增益介质孔径计算与其两边透镜的焦距有关
            aperture=aperture_gain(angle,data['modelAttributeList'][1]['focalLength'],item['radius']*np.cos(angle),sampling_num,delta)
            #计算的结果放入GPU中去储存
            aperture_all.append(aperture.astype(cp.float32))
        else :
            continue
    return aperture_all