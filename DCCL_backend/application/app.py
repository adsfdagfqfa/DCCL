from flask import Flask
#from .extensions import db
from application.config import current_config
import application.handlers as handlers
from application.extensions import redis_client
import logging
from logging.handlers import RotatingFileHandler

def create_app(config_class=current_config):
    app = Flask(__name__)
    #应用配置
    app.config.from_object(config_class)
    configure_logger(app)
    #初始化redis数据库
    redis_client.init_app(app)
    
    with app.app_context():
        handlers.init_app(app)
        #注册蓝图
        
    return app
# def configure_logger(app):

#     log_level = logging.DEBUG if app.debug else logging.INFO

#     # 移除默认的 StreamHandler
#     root_logger = logging.getLogger()
#     for handler in root_logger.handlers[:]:
#         root_logger.removeHandler(handler)

#     # 控制台日志（开发环境）
#     if app.config.get('LOG_TO_CONSOLE', True):
#         console_handler = logging.StreamHandler()
#         console_handler.setFormatter(logging.Formatter(
#             '%(asctime)s %(levelname)s: %(message)s [%(pathname)s:%(lineno)d]'
#         ))
#         console_handler.setLevel(log_level)
#         root_logger.addHandler(console_handler)

#     # 文件日志（生产环境）
#     if app.config.get('LOG_TO_FILE', False):
#         file_handler = RotatingFileHandler(
#             'logs/app.log',
#             maxBytes=1024 * 1024 * 10,  # 10 MB
#             backupCount=10,
#             encoding='utf-8'
#         )
#         file_handler.setFormatter(logging.Formatter(
#             '%(asctime)s %(levelname)s: %(message)s [%(pathname)s:%(lineno)d]'
#         ))
#         file_handler.setLevel(log_level)
#         root_logger.addHandler(file_handler)

#     # 设置根日志级别
#     root_logger.setLevel(log_level)
def configure_logger(app):
    log_level = logging.DEBUG if app.debug else logging.INFO
    fmt = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [%(pathname)s:%(lineno)d]'
    )

    # 控制台
    if app.config.get('LOG_TO_CONSOLE', True):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(fmt)
        console_handler.setLevel(log_level)
        logging.getLogger().addHandler(console_handler)
    else:
        console_handler = None

    # 文件
    file_handler = None
    if app.config.get('LOG_TO_FILE', False):
        os.makedirs('logs', exist_ok=True)
        file_handler = RotatingFileHandler(
            'logs/app.log',
            maxBytes=10 * 1024 * 1024,
            backupCount=10,
            encoding='utf-8'
        )
        file_handler.setFormatter(fmt)
        file_handler.setLevel(log_level)
        logging.getLogger().addHandler(file_handler)

    # Flask / Werkzeug 统一挂 handler
    for name in ('flask.app', 'werkzeug'):
        logger = logging.getLogger(name)
        logger.handlers.clear()
        logger.setLevel(log_level)
        if file_handler:
            logger.addHandler(file_handler)
        if console_handler:
            logger.addHandler(console_handler)
if __name__ == '__main__':
    app = create_app()
    app.run()