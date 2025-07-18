import numpy as np
import cupy as cp
from .aperture_calculation import cal_all_aperture
from .transfer_matrix_calculation import cal_all_matrix
from .steady_state_calculation import cal_final_output
import logging
logger= logging.getLogger(__name__)
class SimulationPipeline:
    def __init__(self, input_data,task_id,iteration_count):
        self.input_data = input_data
        self.task_id = task_id
        self.iteration_count = iteration_count

    def run(self):
        logger.debug(str(self.input_data))
        angle_2=np.abs(self.input_data['angle'][5])*np.pi/180
        angle_1=np.arctan(self.input_data['modelAttributeList'][5]['focalLength']/self.input_data['modelAttributeList'][3]['focalLength']*np.tan(angle_2))
        # print(angle_1)
        # print(angle_2)
        r_max = max(item['radius'] for item in self.input_data['modelAttributeList'])
        # 1.计算所有的孔径函数
        aperture_all=cal_all_aperture(self.input_data,r_max,angle_1,angle_2)
        # 2.计算空间传输矩阵
        matrix_all=cal_all_matrix(self.input_data,r_max,angle_1,angle_2)
        # log_gpu_memory('3')
        logger.info("传输矩阵与有效反射面计算结束")
        generator= cal_final_output(matrix_all,aperture_all,self.input_data,self.task_id,self.iteration_count)
        try:
            while True:
                value = next(generator)
                yield value
        except StopIteration as e:
            # 捕获steay_state最终返回值
            yield e.value
    def update_input_data(self, new_data):
        self.input_data = new_data