from flask import Flask
#from .extensions import db
from config import Config
import handlers

def create_app(config_class=Config):
    app = Flask(__name__)
    #应用配置
    app.config.from_object(config_class)

    with app.app_context():
        handlers.init_app(app)
        #注册蓝图
        
    return app

if __name__ == '__main__':
    app = create_app()
    print(app.url_map)
    app.run()