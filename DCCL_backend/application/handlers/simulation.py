from datetime import datetime
import uuid,time,cupy as cp
import jwt,json
from flask import Response, request, make_response,g
from .base import routes
from application.utils.utility_function import generate_jwt_token, verify_jwt_token,get_uuid_from_token,format_string
from application.extensions import redis_client
from application.utils.redis_utils import get_redis_data, set_redis_data
# from application.config import Config
from application.services.dccl_simulation.pipeline import SimulationPipeline
from application.services.dccl_simulation.task import Task, TaskStatus
import redis
from application.config import Config


import logging
logger = logging.getLogger(__name__)
@routes.route("/today",methods=['GET'])
def test():
    return datetime.today().strftime('%Y-%m-%d %H:%M:%S')


# @routes.route("/simulation",methods=['POST'])
# def simulation():
#     # param = request.args.get('param'),对于get请求，参数在url中
#     # param = request.form.get('param'),对于post请求，参数在body中
#     # encoded_data = request.args.get('data')
#     # json_data = json.loads(encoded_data)  # 解码并解析JSON字符串
#     json_data = request.json  # 获取JSON数据
#     logger.info("json_data:%s",json_data)
#     # token = request.cookies.get('token')
#     # logger.info('token:%s',token)
#     #先检查是否有token
#     # if not token or not verify_jwt_token(token):
#     #     resp = make_response('参数未上传')
#     #     return resp
    
   
#     if not g.user_id:
#         resp = make_response('没有在token中找到用户id,请重新上传参数')
#         logger.info('没有在token中找到用户id,请重新上传参数')
#         return resp
#     data = json.loads(get_redis_data(g.user_id))
#     logger.info("data:%s",data)
#     simulation_pipeline = SimulationPipeline(data, user_id,json_data['iterationCount'])
#     #查看json_data中是否有'path'和'vectors'字段
#     if 'path' not in json_data or 'vectors' not in json_data:
#         logger.info("not json_data")
#         def generate_events(data):
            
#             generator = simulation_pipeline.run()
#             try:
#                 while True:
#                     item = next(generator)
#                     item['selectedAttribute'] = {}
#                     str1 = json.dumps(item, ensure_ascii=False)
#                     yield format_string(str1)
#             except StopIteration as e:
#                 final_value = e.value  # 获取最终返回值
#                 logger.info('final_value:%s',final_value)
#                 final_value['selectedAttribute']={}
#                 cp.get_default_memory_pool().free_all_blocks()
#                 yield format_string(json.dumps(final_value, ensure_ascii=False)) 
#         return Response(generate_events(data),mimetype='text/event-stream')
#     else:
#         #暂定
#         path = json_data.get('path')
#         vectors = json_data.get('vectors')
#         logger.info("json_data:%s",json_data)
#         def generate_events(data):
#             from jsonpath_ng import parse
#             jsonpath_expr = parse(path)
#             for i in vectors:
#                 jsonpath_expr.update(data,i)
#                 key = jsonpath_expr.find(data)[0].path.fields[-1]#获取键名
#                 simulation_pipeline.update_input_data(data)  # 更新输入数据
#                 generator = simulation_pipeline.run()
#                 try:
#                     while True:
#                         item = next(generator)
#                         item['selectedAttribute'] = {key:i}
#                         str1=json.dumps(item,ensure_ascii=False)
#                         yield format_string(str1) 
#                 except StopIteration as e:
#                     final_value = e.value  # 捕获最后返回的数据
#                     logger.info('final_value:%s',final_value)
#                     final_value['selectedAttribute'] = {key:i}
#                     cp.get_default_memory_pool().free_all_blocks()#释放现存
#                     yield format_string(json.dumps(final_value, ensure_ascii=False))
#         return Response(generate_events(data),mimetype='text/event-stream')
        # return request.args.get('param')

@routes.route("/simulation",methods=['POST'])
def simulation():
    json_data = request.json  # 获取JSON数据
    logger.info("json_data:%s",str(json_data))
    if not g.user_id:
        resp = make_response('没有在token中找到用户id,请重新上传参数')
        logger.info('没有在token中找到用户id,请重新上传参数')
        return resp
    task=Task(task_id=json_data['taskID'],redis_client=redis_client, meta_param=json_data)
    task.start()
    resp = make_response('任务已开始')
    return resp



@routes.route("/uploadParameter",methods=['POST'])
def upload_parameter():
    #获取前端发送的数据,字典类型
    data = request.json 
    if not g.user_id:
        # 生成新用户
        return make_response('token未上传或验证失败，请重新上传参数', 400)
    task=Task(redis_client=redis_client, params=data)
    task.save()
    logger.info("用户:%s 上传参数成功保存",g.user_id)

    data = {
        "message": "参数更新成功",
    }
    data['task_id'] = task.task_id

    resp = make_response(data, 200)
    return resp

@routes.route("/stream",methods=['GET'])
def stream():
    task_id = request.args.get('taskID') 
    def result_stream():
        try:
            r = redis.from_url(Config.REDIS_URL)
            pubsub = r.pubsub()
            # pubsub = conn.pubsub()
            pubsub.subscribe('task_progress')
            for msg in pubsub.listen():
                if msg['type'] != 'message':
                    continue
                data = json.loads(msg['data'])
                if data.get('task_id') == task_id:   # 手动过滤
                    try:
                        # yield format_string(data)
                        yield format_string(data.get('progress', {}))
                    except (IOError, BrokenPipeError, ConnectionResetError):
                        # 客户端断开,自动取消任务
                        Task(task_id=task_id, redis_client=redis_client).cancel()
                        break    
                    if data['status'] in (TaskStatus.FINISHED, TaskStatus.ERROR, TaskStatus.CANCELLED):
                        break
        except redis.ConnectionError:
            yield format_string('Connection error')
    # return  Response(result_stream(), mimetype="text/event-stream")
    # 创建 Response 对象
    response = Response(result_stream(), mimetype='text/event-stream', direct_passthrough=True)
    return response


@routes.route('/sse')
def sse():
    """SSE 路由"""
    def generate_events():
        """生成事件数据"""
        while True:
            time.sleep(2)  # 每2秒发送一次事件
            yield f"data: The current time is: {time.ctime()}\n\n"
    return Response(generate_events(), mimetype='text/event-stream')



@routes.route("/task/pause",methods=['GET'])
def pause():
    task_id = request.args.get('taskID') 
    if not task_id:
        return make_response('任务ID未提供', 400)
    try:
        task = Task(task_id=task_id, redis_client=redis_client)
        task.pause()
        return make_response('任务已暂停', 200)
    except Exception as e:
        logger.error(f"暂停任务失败: {e}")
        return make_response('暂停任务失败', 500)
   

@routes.route("/task/cancel",methods=['GET'])
def cancel():
    task_id = request.args.get('taskID') 
    if not task_id:
        return make_response('任务ID未提供', 400)
    try:
        task = Task(task_id=task_id, redis_client=redis_client)
        task.cancel()
        return make_response('任务已取消', 200)
    except Exception as e:
        logger.error(f"取消任务失败: {e}")
        return make_response('取消任务失败', 500)

@routes.route("/task/continue",methods=['GET'])
def _continue():
    task_id = request.args.get('taskID') 
    if not task_id:
        return make_response('任务ID未提供', 400)
    try:
        task = Task(task_id=task_id, redis_client=redis_client)
        task.continue_task()  
        return make_response('任务继续', 200)
    except Exception as e:
        logger.error(f"继续任务失败: {e}")
        return make_response('继续任务失败', 500)