import numpy as np
from .aperture import cal_all_aperture
from .transfer_matrix import cal_all_matrix
from .steady_state_calculation import cal_final_output

def dccl_simulation(data):
    #这里直接写死的，针对dccl结构的
    angle_2=np.abs(data['angle'][5])
    angle_1=np.arctan(data['modelAttributeList'][5]['focalLength']/data['modelAttributeList'][3]['focalLength']*np.tan(angle_2))
    r_max = max(item['radius'] for item in data['modelAttributeList'])
    aperture_all=cal_all_aperture(data,r_max,angle_1,angle_2)
    matrix_all=cal_all_matrix(data,r_max,angle_1,angle_2)

    print("传输矩阵与有效反射面计算结束")
    # for item in aperture_all:
    #     print(type(item)) 
    # for item in matrix_all:
    #     print(type(item)) 
    # <class 'cupy.ndarray'>
    # <class 'cupy.ndarray'>
    # <class 'cupy.ndarray'>
    # <class 'cupy.ndarray'>
    # <class 'cupy.ndarray'>
    # <class 'cupy.ndarray'>
    # <class 'cupy.ndarray'>

    generator= cal_final_output(matrix_all,aperture_all,data)
    try:
        while True:
            value = next(generator)
            yield str(value)
    except StopIteration as e:
        # 捕获steay_state最终返回值
        yield str(e.value)
   