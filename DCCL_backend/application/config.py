class Config:
    # 基本配置
    DEBUG = False
    TESTING = False
    #JWT密钥
    SECRET_KEY = 'intracavity_laser_simulation_system'  
    
    # 数据库配置
    
    #Redis数据库的URL，格式为redis://:password@localhost:6379/0
    REDIS_URL = "redis://192.168.2.128:6379/0"

    
    

    
    
