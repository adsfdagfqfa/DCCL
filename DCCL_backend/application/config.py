import logging
from pathlib import Path
class Config:
    # 基本配置
    # DEBUG = False
    # TESTING = False
    #JWT密钥
    SECRET_KEY = 'intracavity_laser_simulation_system'  
    # RESULT_PATH= 'application/services/dccl_simulation/results'  # 结果存储路径
   

    # config.py 所在目录 = application/
    _CONFIG_DIR = Path(__file__).resolve().parent

    # 目标目录：application/services/dccl_simulation/results
    RESULT_PATH = _CONFIG_DIR / "services" / "dccl_simulation" / "results"
    # 数据库配置
    
    #Redis数据库的URL，格式为redis://:password@localhost:6379/0
    REDIS_URL = "redis://:2151767@127.0.0.1:6379/0"
    REDIS_DEFAULT_EXPIRE = 18000  # 5 小时
    #REDIS_URL = "redis://:2151767@127.0.0.1:6379/0"
     # 日志配置
    LOG_TO_CONSOLE = True   # 开发环境输出到控制台
    LOG_TO_FILE = False     # 开发环境不写入文件

class ProductionConfig(Config):
    LOG_TO_CONSOLE = False
    LOG_TO_FILE = True
    LOG_LEVEL = logging.INFO

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG

# 显式指定当前环境
current_env = 'development'  # 'production'


# 根据指定的环境加载对应的配置
if current_env == 'development':
    current_config = DevelopmentConfig()
else:
    current_config = ProductionConfig()


    
    
