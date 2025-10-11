from datetime import datetime
import uuid,time
import jwt,json
from flask import Response, request, make_response,g,current_app as app
from application.utils.utility_function import generate_jwt_token, verify_jwt_token,get_uuid_from_token,format_string
from .base import routes
import logging
logger = logging.getLogger(__name__)
@routes.route('/token/init', methods=['POST'])
def token_init():
   
    if hasattr(g, 'user_id') and g.user_id:
        return make_response('用户已存在', 400)
    # 生成新用户
    user_id = str(uuid.uuid4())
    new_token = generate_jwt_token(user_id)
    logger.info("新用户:%s",user_id)

    # 动态取客户端请求的 Host，去掉端口
    # host = request.headers.get('Host', 'localhost')        # 1.94.185.7:12000
    # domain = host.split(':')[0]   
    domain = None
    if app.config.get('ENV') == 'production':          # 或者任意你定义的标志
        host = request.headers.get('Host', '')
        domain = host.split(':')[0]
        # domain = f'.{domain}' if domain != 'localhost' else None

    secure_flag = request.is_secure
    resp = make_response('token生成成功')
    resp.set_cookie(
        'token',
        new_token,
        httponly=True,
        secure=secure_flag,     # True（HTTPS）/False（HTTP）
        samesite='Lax',
        domain=domain,        # 设置为请求的域名，允许子域名共享cookie
        path='/'
    )
    return resp
    