import uuid
import json
import redis
import time
from application.utils.utility_function import generate_task_id,save_bytes_to_file
from application.config import Config
from .pipeline import SimulationPipeline
import logging
import threading
import gc,cupy as cp
from application.config import Config
logger = logging.getLogger(__name__)
class TaskStatus:
    PENDING = 'pending'
    RUNNING = 'running'
    CANCELLED = 'cancelled'
    FINISHED = 'finished'
    ERROR = 'error'
    PAUSED = 'paused'


class Task:
    def __init__(self, task_id=None, redis_client = None,params={},meta_param={}):
        self.task_id = task_id or generate_task_id()  # 默认生成新任务 ID
        self.redis_client = redis_client # Redis 客户端实例
        self.status = TaskStatus.PENDING
        self.result_path =[]  # 结果存储路径
        self.params = params
        self.sweep= meta_param['variable'] if 'variable' in meta_param else {}
        self.iteration_count = meta_param['iterationCount'] if 'iterationCount' in meta_param else 1
        self._load()  # 加载任务数据（如果已存在）

    def _load(self):
        #从 Redis 加载任务数据（如果存在）"""
        if self.redis_client.exists(self.task_id):
            logger.debug(f"Loading task {self.task_id} from Redis.")
            status_bytes = self.redis_client.hget(self.task_id, 'status')
            self.status = status_bytes.decode() if status_bytes else TaskStatus.PENDING

            params_bytes = self.redis_client.hget(self.task_id, 'params')
            self.params = json.loads(params_bytes.decode()) if params_bytes else {}

            sweep_bytes = self.redis_client.hget(self.task_id, 'sweep')
            self.sweep = json.loads(sweep_bytes.decode()) if sweep_bytes else {}
            
            result_path_bytes = self.redis_client.hget(self.task_id, 'result_path')
            self.result_path = json.loads(result_path_bytes.decode()) if result_path_bytes else []
    
    def save(self):
        #保存任务状态到 Redis
        self.redis_client.hset(self.task_id, mapping={
            "status": self.status,
            "params": json.dumps(self.params),
            "sweep": json.dumps(self.sweep),
            "result_path":  json.dumps(self.result_path),
        })
        self.redis_client.expire(self.task_id, 6 * 60 * 60)  # 设置过期时间（例如6小时）

    def start(self):
        # self.pipeline = SimulationPipeline(params, self.task_id, self.iteration_count)
        self.status = TaskStatus.RUNNING
        self.save()

        # 启动后台线程
        if self.sweep=={}:
            thread = threading.Thread(target=self._run_pipeline_loop)
        else:
            thread = threading.Thread(target=self._run_pipeline_loop_range)
        thread.daemon = True
        thread.start()

    def _run_pipeline_loop(self):
        try:
            pipeline= SimulationPipeline(self.params, self.task_id, self.iteration_count)
            generator = pipeline.run()  # 获取生成器
            r = redis.from_url(Config.REDIS_URL)
            for value in generator:
                current_status = self.redis_client.hget(self.task_id, "status").decode()
                logger.debug(f"[{self.task_id}] current status: {current_status}")
                if current_status == TaskStatus.CANCELLED:
                    logger.info(f"[{self.task_id}] cancelled.")
                    break
                elif current_status == TaskStatus.PAUSED:
                    logger.info(f"[{self.task_id}] paused.")
                    while self.redis_client.hget(self.task_id, "status").decode() == TaskStatus.PAUSED:
                        time.sleep(1)
                    # continue  # 继续执行
                elif current_status != TaskStatus.RUNNING:
                    logger.info(f"[{self.task_id}] unknown state.")
                    break
                #如果value是元组，表示包含了中间结果和两个矩阵的字节流
                if isinstance(value, tuple):
                    file_path_field_distribution_main=Config.RESULT_PATH / f"{self.task_id}" / "field_distribution_main.mat"
                    file_path_field_distribution_free=Config.RESULT_PATH / f"{self.task_id}" / "field_distribution_free.mat"
                    m={}
                    m['field_distribution_main'] = str(file_path_field_distribution_main)
                    m['field_distribution_free'] = str(file_path_field_distribution_free)
                    m['variant']=1
                    self.result_path.append(m)
                    self.save()
                    # 保存字节流到文件
                    save_bytes_to_file(file_path_field_distribution_main, value[1])
                    save_bytes_to_file(file_path_field_distribution_free, value[2])
                    value = value[0]
                # 推送当前进度
                # 收到创建redis连接
                
                # redis_message = {
                #     "task_id": self.task_id,
                #     "status": TaskStatus.RUNNING,
                # }
                value['selectedAttribute'] = {}
                # redis_message['progress']=json.dumps(value)#确保是字符串
                redis_message = RedisMessage(self.task_id, self.status, value).to_json()
                # data = json.dumps(redis_message, ensure_ascii=False)
                
                # r.publish('task_progress',data)
                r.publish('task_progress',redis_message)

            self.redis_client.hset(self.task_id, "status", TaskStatus.FINISHED)
            logger.info(f"[{self.task_id}] finished.")
        except Exception as e:
            self.redis_client.hset(self.task_id, "status", TaskStatus.ERROR)
            logger.exception(f"[{self.task_id}] error: {e}")
        finally:
            # 清理资源
            self._cleanup_resources()

    def _run_pipeline_loop_range(self):
        try:
            from jsonpath_ng import parse
            pipeline=SimulationPipeline(self.params, self.task_id, self.iteration_count)
            path= self.sweep['path']
            vectors = self.sweep['vectors']
            jsonpath_expr = parse(path)
            r = redis.from_url(Config.REDIS_URL)
            for i in vectors:
                jsonpath_expr.update(self.params,i)
                key = jsonpath_expr.find(self.params)[0].path.fields[-1]#获取键名
                pipeline.update_input_data(self.params)  # 更新输入数据
                generator = pipeline.run()
                for value in generator:
                    current_status = self.redis_client.hget(self.task_id, "status").decode()
                    
                    if current_status == TaskStatus.CANCELLED:
                        logger.info(f"[{self.task_id}] cancelled.")
                        break
                    elif current_status == TaskStatus.PAUSED:
                        logger.info(f"[{self.task_id}] paused.")
                        while self.redis_client.hget(self.task_id, "status").decode() == TaskStatus.PAUSED:
                            time.sleep(1)
                        continue  # 继续执行
                    elif current_status != TaskStatus.RUNNING:
                        logger.info(f"[{self.task_id}] unknown state.")
                        break
                    if isinstance(value, tuple):
                        file_path_field_distribution_main=Config.RESULT_PATH / f"{self.task_id}" / "field_distribution_main.mat"
                        file_path_field_distribution_free=Config.RESULT_PATH / f"{self.task_id}" / "field_distribution_free.mat"
                        m={}
                        m['field_distribution_main'] = str(file_path_field_distribution_main)
                        m['field_distribution_free'] = str(file_path_field_distribution_free)
                        m['variant']= i
                        self.result_path.append(m)
                        self.save()
                        save_bytes_to_file(file_path_field_distribution_main, value[1])
                        save_bytes_to_file(file_path_field_distribution_free, value[2])
                        value = value[0]
                    
                    value['selectedAttribute'] = {key:i}
                    redis_message=RedisMessage(self.task_id, self.status, value).to_json()
                    # redis_message.update(value)  # 更新进度信息
                    r.publish('task_progress',redis_message)

            self.redis_client.hset(self.task_id, "status", TaskStatus.FINISHED)
            logger.info(f"[{self.task_id}] finished.")
        except Exception as e:
            self.redis_client.hset(self.task_id, "status", TaskStatus.ERROR)
            logger.exception(f"[{self.task_id}] error: {e}")
        finally:
            # 清理资源
            self._cleanup_resources()


    def cancel(self):
        #取消任务
        self.status = TaskStatus.CANCELLED
        self.save()

    def finish(self, result_path):
        #标记任务完成
        self.status = TaskStatus.FINISHED
        self.result_path = result_path
        self.save()

    def to_dict(self):
        #将任务数据转换为字典（用于返回给前端）
        return {
            "task_id": self.task_id,
            "status": self.status,
            "progress": self.progress,
            "created_at": self.created_at,
            "result_path": self.result_path
        }

    def is_cancelled(self):
        #检查任务是否已取消
        return self.status == TaskStatus.CANCELLED
    
    def pause(self):
        # 暂停任务
        if self.status == TaskStatus.RUNNING:
            self.status = TaskStatus.PAUSED
            self.save()

    def continue_task(self):
        # 继续任务
        if self.status == TaskStatus.PAUSED:
            self.status = TaskStatus.RUNNING
            self.save()
    def _cleanup_resources(self):
        # 让所有缓存的显存块释放回 driver
        cp.get_default_memory_pool().free_all_blocks()
        cp.get_default_pinned_memory_pool().free_all_blocks()

        # 如果还用了FFT计划缓存，也顺手清掉
        cp.fft.config.get_plan_cache().clear()

        # 触发 Python 垃圾回收，确保对象被回收
        gc.collect()

        logger.info(f"[{self.task_id}] CuPy GPU memory released")

class RedisMessage:
    """
    轻量级消息封装：
    RedisMessage(task_id, status, progress).to_json()
    """

    def __init__(self, task_id: str, status: str, progress: any):
        self._data = {
            "task_id": task_id,
            "status": status,
            "progress": json.dumps(progress, ensure_ascii=False)
        }

    def to_json(self) -> str:
        """返回可直接写到 Redis 的 JSON 字符串"""
        return json.dumps(self._data, ensure_ascii=False)

    def to_dict(self) -> dict:
        """如需直接存 dict，也可调用"""
        return self._data