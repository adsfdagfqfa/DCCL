from datetime import datetime
import uuid,time
import jwt,json
from flask import Response, request, make_response
from .base import routes
from application.utils.utilityFunction import generate_jwt_token, verify_jwt_token,get_uuid_from_token,format_string
from application.extensions import redis_client
# from application.config import Config
from application.dccl_simulation import dccl_simulation
from application.extensions import redis_client

@routes.route("/today",methods=['GET'])
def test():
    return datetime.today().strftime('%Y-%m-%d %H:%M:%S')


@routes.route("/simulation",methods=['GET'])
def simulation():
    # param = request.args.get('param'),对于get请求，参数在url中
    # param = request.form.get('param'),对于post请求，参数在body中
    encoded_data = request.args.get('data')
    json_data = json.loads(encoded_data)  # 解码并解析JSON字符串
    
    token = request.cookies.get('token')
    print('token:',token)
    #先检查是否有token
    if not token or not verify_jwt_token(token):
        resp = make_response('参数未上传')
        return resp
    
    user_id=get_uuid_from_token(token)
    print('当前用户:',user_id)
    data = json.loads(redis_client.get(user_id))
    if not json_data:
        # data = json.loads(redis_client.get(user_id))
        print(data)
        print("not json_data")
        def generate_events(data):
            for item in dccl_simulation(data):
                yield format_string(item) 
        return Response(generate_events(data),mimetype='text/event-stream')

        
    else:
        #暂定
        path = json_data.get('path')
        vectors = json_data.get('vectors')
        print("json_data:",json_data)
        print(path)
        print(vectors)
        def generate_events(data):
            from jsonpath_ng import parse
            jsonpath_expr = parse(path)
            for i in vectors:
                jsonpath_expr.update(data,i)
                print('updatedData',data)
                key = jsonpath_expr.find(data)[0].path.fields[-1]#获取键名
                for item in dccl_simulation(data):
                    str1="此时"+key+":"+str(i)+' '+item
                    print(str1)
                    yield format_string(str1) 
        return Response(generate_events(data),mimetype='text/event-stream')
        # return request.args.get('param')


@routes.route("/uploadParameter",methods=['POST'])
def upload_parameter():
    #获取前端发送的数据,字典类型
    data = request.json
    print(data['modelAttributeList'])

    token = request.cookies.get('token')
    print(token)
    if not token or not verify_jwt_token(token):
        # 生成新用户
        user_id = str(uuid.uuid4())
        new_token = generate_jwt_token(user_id)
        print(new_token)
        # 存储基础信息到Redis（示例存储创建时间）
        redis_client.set(user_id, json.dumps(data))
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
        
        user_id = get_uuid_from_token(token)
        # 更新用户信息
        redis_client.set(user_id, json.dumps(data))
        print("用户",user_id,'更新参数')
        resp = make_response('参数更新成功')
        return "参数更新成功"

def generate_events():
    """生成事件数据"""
    while True:
        time.sleep(2)  # 每2秒发送一次事件
        yield f"data: The current time is: {time.ctime()}\n\n"

@routes.route('/sse')
def sse():
    """SSE 路由"""
    return Response(generate_events(), mimetype='text/event-stream')