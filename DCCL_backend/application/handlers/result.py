import uuid,time,io,scipy.io as sio
import jwt,json
from flask import Response, request, make_response,jsonify,g
from .base import routes
from application.utils.utility_function import generate_jwt_token, verify_jwt_token,get_uuid_from_token,format_string,get_redis_data
from application.utils.utility_function import  set_redis_data,decompress
import matplotlib.pyplot as plt
import mpld3

@routes.route("/picture/<string:key>",methods=['GET'])
def getPicture(key):
    token = request.cookies.get('token')
    # user_id=get_uuid_from_token(token)
    if not token or not verify_jwt_token(token):
        resp = make_response('认证错误')
        return resp
    mat_bytes= get_redis_data(key)
    mat_buffer = io.BytesIO(mat_bytes)
    mat_data = sio.loadmat(mat_buffer)['matrix']
    img=plt.imshow(mat_data, cmap='jet', interpolation='nearest')
    plt.colorbar(img)
    html_content=mpld3.fig_to_html(plt.gcf(),template_type='simple')
    plt.close()

    # 返回HTML内容
    return jsonify({'html': html_content})

@routes.route("/download/<string:task_id>",methods=['GET'])
def download(task_id):
    return '下载成功'