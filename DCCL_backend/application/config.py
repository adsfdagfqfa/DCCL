import logging,os
from pathlib import Path
class Config:
    #JWT密钥
    SECRET_KEY = 'W7x9p2k4R8mY3n6qL1t5vC0jX8eF4uS7aB9dG2hN0kP3rQ6wE5yU7iO9zA1bC4dE6fG8hI0jK2lM4nP6qR8sT0uV2wX4yZ6'  
    # RESULT_PATH= 'application/services/dccl_simulation/results'  # 结果存储路径
   

    # config.py 所在目录 = application/
    _CONFIG_DIR = Path(__file__).resolve().parent

    # 目标目录：application/services/dccl_simulation/results
    RESULT_PATH = _CONFIG_DIR / "services" / "dccl_simulation" / "results"
    # 数据库配置
    
    #Redis数据库的URL，格式为redis://:password@localhost:6379/0
    # REDIS_URL = "redis://:123456@redis-service:6379/0"
    REDIS_URL = "redis://:123456@localhost:6379/0"
    REDIS_DEFAULT_EXPIRE = 18000  # 5 小时
     # 日志配置
    # LOG_TO_CONSOLE = True   # 开发环境输出到控制台
    # LOG_TO_FILE = False     # 开发环境不写入文件
    LOG_TO_CONSOLE = True
    LOG_TO_FILE = False
    LOG_CONSOLE_LEVEL = logging.DEBUG   # 控制台日志级别
    LOG_FILE_LEVEL = logging.DEBUG      # 文件日志级别
    LOG_PATH = _CONFIG_DIR / ".." / "logs"  # 日志文件目录

class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    LOG_TO_CONSOLE = False
    LOG_TO_FILE = True
    LOG_CONSOLE_LEVEL = logging.INFO    # 生产控制台只打印 info+
    LOG_FILE_LEVEL = logging.DEBUG      # 文件保留所有日志
    # REDIS_URL = "redis://:123456@redis-service:6379/0"
    REDIS_URL = "redis://:123456@localhost:6379/0"

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    LOG_TO_CONSOLE = True
    LOG_TO_FILE = False
    LOG_CONSOLE_LEVEL = logging.DEBUG   # 本地控制台直接看全量日志

# 映射字符串 → 配置类
config_map = {
    'development': DevelopmentConfig,
    'production':  ProductionConfig,
}

# 如果环境变量没设置，默认 development
current_env = os.getenv('FLASK_ENV', 'development')

# 导出给应用使用
current_config = config_map[current_env]()


    
    
