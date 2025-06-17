import numpy as np
from .aperture import cal_all_aperture
from .transfer_matrix import cal_all_matrix
from .steady_state_calculation import cal_final_output
from application.utils.utility_function import log_gpu_memory
import logging 
logger = logging.getLogger(__name__)
def dccl_simulation(data,user_id):
    #这里直接写死的，针对dccl结构的
    angle_2=np.abs(data['angle'][5])*np.pi/180
    angle_1=np.arctan(data['modelAttributeList'][5]['focalLength']/data['modelAttributeList'][3]['focalLength']*np.tan(angle_2))
    print(angle_1)
    print(angle_2)
    r_max = max(item['radius'] for item in data['modelAttributeList'])
    # log_gpu_memory('1')
    aperture_all=cal_all_aperture(data,r_max,angle_1,angle_2)
    # log_gpu_memory('2')
    matrix_all=cal_all_matrix(data,r_max,angle_1,angle_2)
    # log_gpu_memory('3')
    logger.info("传输矩阵与有效反射面计算结束")

    generator= cal_final_output(matrix_all,aperture_all,data,user_id)
    try:
        while True:
            value = next(generator)
            yield value
    except StopIteration as e:
        # 捕获steay_state最终返回值
        return e.value
   