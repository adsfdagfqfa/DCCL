from flask import Flask
#from .extensions import db
from application.config import Config
import application.handlers as handlers
from application.extensions import redis_client


def create_app(config_class=Config):
    app = Flask(__name__)
    #应用配置
    app.config.from_object(config_class)
    #初始化redis数据库
    redis_client.init_app(app)
    
    with app.app_context():
        handlers.init_app(app)
        #注册蓝图
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()