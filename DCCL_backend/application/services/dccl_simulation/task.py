import uuid
import json
import time
import redis

class TaskStatus:
    PENDING = 'pending'
    RUNNING = 'running'
    CANCELLED = 'cancelled'
    FINISHED = 'finished'
    ERROR = 'error'


class Task:
    def __init__(self, task_id=None, redis_conn=None):
        self.task_id = task_id or str(uuid.uuid4())  # 默认生成新任务 ID
        self.redis = redis_conn or redis.StrictRedis(decode_responses=True)
        self.key = f"task:{self.task_id}"  # Redis 键名
        self.status = TaskStatus.PENDING
        self.progress = 0.0
        self.result_path = None
        self.params = {}
        self.created_at = time.time()
        self._load()  # 加载任务数据（如果已存在）

    def _load(self):
        """从 Redis 加载任务数据（如果存在）"""
        if self.redis.exists(self.key):
            data = self.redis.hgetall(self.key)
            self.status = data.get("status", TaskStatus.PENDING)
            self.params = json.loads(data.get("params", "{}"))
            self.progress = float(data.get("progress", 0.0))
            self.result_path = data.get("result_path")
            self.created_at = float(data.get("created_at", time.time()))
    
    def save(self):
        """保存任务状态到 Redis"""
        self.redis.hset(self.key, mapping={
            "status": self.status,
            "params": json.dumps(self.params),
            "progress": self.progress,
            "result_path": self.result_path or "",
            "created_at": self.created_at
        })
        self.redis.expire(self.key, 6 * 60 * 60)  # 设置过期时间（例如6小时）

    def start(self, params):
        """启动任务"""
        self.status = TaskStatus.RUNNING
        self.params = params
        self.progress = 0.0
        self.created_at = time.time()
        self.save()

    def update_progress(self, value):
        """更新任务的进度"""
        self.progress = value
        self.save()

    def cancel(self):
        """取消任务"""
        self.status = TaskStatus.CANCELLED
        self.save()

    def finish(self, result_path):
        """标记任务完成"""
        self.status = TaskStatus.FINISHED
        self.result_path = result_path
        self.save()

    def to_dict(self):
        """将任务数据转换为字典（用于返回给前端）"""
        return {
            "task_id": self.task_id,
            "status": self.status,
            "progress": self.progress,
            "created_at": self.created_at,
            "result_path": self.result_path
        }

    def is_cancelled(self):
        """检查任务是否已取消"""
        return self.status == TaskStatus.CANCELLED
