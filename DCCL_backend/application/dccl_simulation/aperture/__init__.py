from aperture_cateye import aperture_cateye
from aperture_gain import aperture_gain
import cupy as cp
import numpy as np
def cal_all_aperture(data,r_max,angle_1,angle_2):

    aperture_all=[]

    for (index,item) in data['modelAttributeList']:
        
        angle = angle_1 if index<=4 else angle_2
        #判断是镜子还是介质
        if item['type']=='lens' :
            aperture=aperture_cateye(angle,item['focalLength'],item['radius'],r_max)
            #计算的结果都放入GPU中去储存
            aperture_all.append(cp.asarray(aperture.astype(np.float32)))

        elif item['type']=='medium':
            #这里同样写死第二个参数，由于增益介质孔径计算与其两边透镜的焦距有关
            aperture=aperture_gain(angle,data['modelAttributeList'][1]['focalLength'],item['radius']*np.cos(angle),r_max)
            #计算的结果放入GPU中去储存
            aperture_all.append(cp.asarray(aperture.astype(np.float32)))
        else :
            continue
    return aperture_all

