from flask import Blueprint,g, request
from application.utils.utility_function import verify_jwt_token, get_uuid_from_token
#base = Blueprint('base', __name__, url_prefix='/base')
#'base'标识蓝图名称，可用于url_for函数
#__name__标识模块名称
#prefix标识url前缀
routes = Blueprint('base', __name__,url_prefix='/api/v1')
import logging
logger = logging.getLogger(__name__)
#在每个请求处理之前保存用户id到g对象中
# g对象是一个特殊的对象，用于存储请求上下文中的数据
# 在请求处理函数中可以通过g.user_id访问保存的用户id
@routes.before_request
def load_user_id():
    # 从请求头中获取 JWT 令牌
    token = request.cookies.get('token')
    logger.debug('token:%s', token)
    logger.debug('verify:%s', verify_jwt_token(token))
    if not token or not verify_jwt_token(token):
        g.user_id = None
    else:
        user_id = get_uuid_from_token(token)
        if user_id:
            g.user_id = user_id
        else:
            g.user_id = None
   
        