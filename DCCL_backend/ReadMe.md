# 同济大学毕业设计 
## 腔内激光的动态多模分析工具后端
需要安装的包如requirements.txt文件所示，运行一下代码安装包
``` 
pip install -r requirements.txt
```

需要注意的是代码中需要使用到Cupy来进行GPU加速，但是截至2025年5月2日，CuPy官方版本未引入lambertW函数
需要安装预发布v14.0.0a1版本，下载链接为：https://github.com/cupy/cupy/releases/download/v14.0.0a1/cupy_cuda11x-14.0.0a1-cp310-cp310-manylinux2014_x86_64.whl

运行以下代码安装CuPy
```
pip install cupy_cuda11x-14.0.0a1-cp310-cp310-manylinux2014_x86_64.whl
```