
from datetime import datetime
import uuid,time
import jwt,json
from flask import Response, request, make_response,g
from application.utils.utility_function import generate_jwt_token, verify_jwt_token,get_uuid_from_token,format_string
from .base import routes
import logging
logger = logging.getLogger(__name__)
@routes.route('/token/init', methods=['POST'])
def token_init():
   # 生成新用户
    user_id = str(uuid.uuid4())
    new_token = generate_jwt_token(user_id)
    logger.info("新用户:%s",user_id)
    resp = make_response('token生成成功')
    resp.set_cookie(
        'token',
        new_token,
        httponly=True,
        secure=True,  # 生产环境必须开启
        samesite='Lax'
    )
    return resp
    