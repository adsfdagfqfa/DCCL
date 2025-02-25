from datetime import datetime
import uuid
import jwt
from flask import request, make_response
from .base import routes
from application.utils.utilityFunction import generate_jwt_token, verify_jwt_token
from application.extensions import redis_client
from application.config import Config
@routes.route("/today",methods=['GET'])
def test():
    return datetime.today().strftime('%Y-%m-%d %H:%M:%S')


@routes.route("/simulation",methods=['GET'])
def simulation():
    # param = request.args.get('param'),对于get请求，参数在url中
    # param = request.form.get('param'),对于post请求，参数在body中
    if(len(request.args)==0):
        return "no param"
    else:
        return request.args.get('param')
    return datetime.today().strftime('%Y-%m-%d %H:%M:%S')   


@routes.route("/uploadParameter",methods=['POST'])
def upload_parameter():
    #将前端发送的数据转换为字典
    form_data=request.form.to_dict()
    print(form_data.get('payload'))
    token = request.cookies.get('token')
    print(token)
    if not token or not verify_jwt_token(token):
        # 生成新用户
        user_id = str(uuid.uuid4())
        new_token = generate_jwt_token(user_id)
        print(new_token)
        # 存储基础信息到Redis（示例存储创建时间）
        redis_client.set(user_id, form_data.get('payload'))
        print("新用户",user_id)
        
        # 设置Cookie,以便于后续访问直接通过Cookie验证
        resp = make_response('参数上传成功')
        resp.set_cookie(
            'token',
            new_token,
            httponly=True,
            secure=True,  # 生产环境必须开启
            samesite='Lax'
        )
        return resp
    else:
        # 获取用户信息
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms='HS256')
        user_id = payload['uuid']
        # 更新用户信息
        redis_client.set(user_id, form_data.get('payload'))
        print("用户",user_id,'更新参数')
        resp = make_response('参数更新成功')
        return "参数更新成功"   