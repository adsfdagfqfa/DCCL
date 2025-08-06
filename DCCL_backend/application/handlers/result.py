import uuid,time,io,scipy.io as sio
import jwt,json,numpy as np
from flask import Response, request, make_response,jsonify, send_file
import jwt,json
from flask import Response, request, make_response,jsonify,g
from .base import routes
from application.utils.utility_function import generate_jwt_token, verify_jwt_token,get_uuid_from_token,format_string
from application.utils.redis_utils import get_redis_data, set_redis_data
from application.config import current_config
import matplotlib 
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
import mpld3
from pathlib import Path

@routes.route("/picture/<string:taskID>/<string:fileName>",methods=['GET'])
def getPicture(taskID,fileName):
    if not g.user_id:
        # 生成新用户
        return make_response('token未上传或验证失败，请重新上传参数', 400)
    # mat_bytes= get_redis_data(path)
    # mat_buffer = io.BytesIO(mat_bytes)
    # mat_data = np.abs(sio.loadmat(mat_buffer)['matrix'])
    safe_root = Path(current_config.RESULT_PATH).resolve()
    safe_path = (safe_root / taskID / fileName).resolve()
    if not safe_root in safe_path.parents or not safe_path.exists():
        return make_response('文件不存在或路径不安全', 500)
         
    mat_data =np.abs(sio.loadmat(safe_path)['matrix'])
    plt.figure()
    img=plt.imshow(mat_data, cmap='jet', interpolation='nearest')
    plt.colorbar(img)
    html_content=mpld3.fig_to_html(plt.gcf(),template_type='simple')
    plt.close()

    # 返回HTML内容
    return jsonify({'html': html_content})

@routes.route("/download/<string:taskID>/<string:fileName>",methods=['GET'])
def download(taskID,fileName):
    # token = request.cookies.get('token')
    # user_id=get_uuid_from_token(token)
    # if not token or not verify_jwt_token(token):
    #     resp = make_response('认证错误')
    #     return resp
    # mat_bytes= get_redis_data(key_id)
    # mat_buffer = io.BytesIO(mat_bytes)
    # mat_buffer.seek(0)  # 确保指针在文件开头

    # # 设置 MIME 类型和文件名
    # mimetype = "application/octet-stream"  # 通用二进制文件类型
    # filename = f"file.mat"  # 客户端看到的文件名，带 .mat 扩展名

    # return send_file(mat_buffer, mimetype=mimetype, as_attachment=True, download_name=filename)
    if not g.user_id:
   
        return make_response('token未上传或验证失败，请重新上传参数', 400)
    safe_root = Path(current_config.RESULT_PATH).resolve()
    safe_path = (safe_root / taskID / fileName).resolve()

    if not safe_root in safe_path.parents or not safe_path.exists():
        return make_response('文件不存在或路径不安全', 500)

    return send_file(
        safe_path,
        # mimetype="application/octet-stream",
        as_attachment=True,
        download_name=fileName
    )