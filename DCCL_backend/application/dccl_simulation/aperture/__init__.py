from aperture_cateye import aperture_cateye
from aperture_gain import aperture_gain
import math
import cupy as cp
def cal_all_aperture(data,r_max):

    #这里是直接写死的，针对dccl结构的
    angle_2=get_angle(data['modelAttributeList'][5]['focalLength'],
                      data['modelAttributeList'][6]['focalLength'],
                      data['distance'][5],data['angle'][5])
    angle_1=math.atan(data['modelAttributeList'][5]['focalLength']/data['modelAttributeList'][3]['focalLength']*math.tan(angle_2))

    aperture_all={}

    for (index,item) in data['modelAttributeList']:
        #判断是镜子还是介质
        angle = angle_1 if index<=4 else angle_2
        if item['type']=='lens' :
            aperture=aperture_cateye(angle,item['focalLength'],item['radius'],r_max)
            #计算的结果都放入GPU中去储存
            aperture_all[item['model']]=cp.asarray(aperture.astype(float32))

        else item['type']=='medium':
            #这里同样写死第二个参数，由于增益介质孔径计算与其两边透镜的焦距有关
            aperture=aperture_gain(angle,data['modelAttributeList'][1]['focalLength'],item['radius']*math.cos(angle),r_max)
            #计算的结果放入GPU中去储存
            aperture_all[item['model']]=cp.asarray(aperture.astype(float32))
        else
            continue
    return aperture_all

#专门计算dccl系统自由空间腔的光线入射角度
def get_angle(f1,f2,d,theta):
    d1=d-f1-f2
    return math.abs(math.atan(d*math.tan(theta)/d1))

