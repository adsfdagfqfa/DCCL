from pathlib import Path
from typing import Union
import jwt  
import cupy as cp
import time
import datetime
import application.config as config
from application.extensions import redis_client
import msgpack,zlib,numpy as np
from scipy.sparse import csr_matrix
import logging
from scipy.io import savemat
import random
import string

logger = logging.getLogger(__name__)
def generate_jwt_token(uuid, algorithm='HS256'):

    payload = {
        'uuid': uuid,  # User ID
        'iat': datetime.datetime.now(datetime.timezone.utc),  # Token issuance time
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24),
    }
   
    secret_key = config.Config.SECRET_KEY
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token

def verify_jwt_token(token):
    # 验证现有Token
    try:
        #设置时间容错
        leeway = datetime.timedelta(minutes=5)
        payload = jwt.decode(token, config.Config.SECRET_KEY, algorithms='HS256', leeway = leeway)
        uuid = payload['uuid']
        # 检查Redis是否存在用户记录（可选）
        if not redis_client.exists(uuid):
            # 数据过期
            return False
        return True
    except jwt.ExpiredSignatureError:
        # Token过期
        # print("Token has expired")
        return False
    except jwt.InvalidTokenError as e:
        # 非法Token
        # print(f"Invalid token: {e}")
        return False
    
#从token中提取uuid
def get_uuid_from_token(token):
    leeway = datetime.timedelta(minutes=5)
    payload = jwt.decode(token, config.Config.SECRET_KEY, algorithms='HS256', leeway = leeway)
    uuid = payload['uuid']
    return uuid
      
#将字符串变量修改为sse的格式
def format_string(value):
    return "data: "+str(value)+"\n\n"


#将CSR格式的稀疏矩阵转换为字典
def csr_matrix_to_dict(csr):
    return {
        #光场包含复数，需要分开存储实部和虚部
        'data_real': csr.data.real.tolist(),
        'data_imag': csr.data.imag.tolist(),
        "indices": csr.indices.tolist(),
        "indptr": csr.indptr.tolist(),
        "shape": csr.shape
    }
def dict_to_csr_matrix(csr_dict):
    data_real = np.array(csr_dict['data_real'])
    data_imag = np.array(csr_dict['data_imag'])
    indices = np.array(csr_dict['indices'])
    indptr = np.array(csr_dict['indptr'])
    shape = csr_dict['shape']
    data = data_real + 1j * data_imag
    return csr_matrix((data, indices, indptr), shape=shape)

def compress(data):
    compressed = zlib.compress(msgpack.packb(data))
    return compressed

def decompress(data):
    packed = zlib.decompress(data)
    return msgpack.unpackb(packed)
  

def log_gpu_memory(label="", file=None):
    """
    记录当前 GPU 显存占用
    Args:
        label (str): 监控点标签（如 "After U1 calculation"）
        file (str): 输出文件名（None 则打印到控制台）
    """
    # 获取 CuPy 内存池状态
    pool = cp.get_default_memory_pool()
    used = pool.used_bytes()       # 已用显存（字节）
    free = pool.free_bytes()       # 空闲显存（字节）
    total = used + free            # 总显存（通常等于 GPU 总显存）
    
    # 转换为易读格式
    used_mb = used / 1024**2
    free_mb = free / 1024**2
    total_mb = total / 1024**2
    
    # 生成日志信息
    timestamp = time.strftime("%H:%M:%S", time.localtime())
    log_msg = (
        f"[{timestamp}] {label}\n"
        f"  Used: {used_mb:.2f} MB\n"
        f"  Free: {free_mb:.2f} MB\n"
        f"  Total: {total_mb:.2f} MB\n"
        "-----------------------"
    )
    
    # 输出到文件或控制台
    if file:
        with open(file, "a") as f:
            f.write(log_msg + "\n")
    else:
        logger.info(log_msg)


def save_mat(cupy_matrix):


    numpy_matrix = cp.asnumpy(cupy_matrix)

    # 将 numpy 矩阵保存为 .mat 文件
    savemat("matrix.mat", {"matrix": numpy_matrix})

    print("矩阵已成功保存为 matrix.mat 文件")



def generate_task_id(prefix="task", random_length=6):
    """
    生成唯一的任务 ID，格式: task_时间戳_随机串
    Args:
        prefix (str): 可选前缀（如 task、sim、job）
        random_length (int): 随机字符串的长度，建议 4~8 位
    Returns:
        str: 格式如 task_1720081234567_a1b2c3
    """
    timestamp = int(time.time() * 1000)  # 毫秒时间戳，13 位
    rand_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random_length))
    return f"{prefix}_{timestamp}_{rand_part}"

def save_bytes_to_file(path: Union[str, Path], data: bytes) -> Path:
    """
    将字节流写入指定路径的文件。
    Args:
        path : str 或 pathlib.Path 目标文件路径。如果目录不存在会自动创建。
        data : bytes 待写入的字节流。
    Returns:
        pathlib.Path写入后的文件路径（绝对路径）。
    """
    path = Path(path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)  # 递归创建目录
    with path.open("wb") as f:
        f.write(data)
    return path