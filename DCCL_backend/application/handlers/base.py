from flask import Blueprint

#base = Blueprint('base', __name__, url_prefix='/base')
#'base'标识蓝图名称，可用于url_for函数
#__name__标识模块名称
#prefix标识url前缀
routes = Blueprint('base', __name__, url_prefix='/api/v1')