from flask import Flask
from pathlib import Path
#from .extensions import db
from application.config import current_config
import application.handlers as handlers
from application.extensions import redis_client
import logging,sys
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

def configure_logger(app: Flask):
    """配置日志系统"""
    log_dir: Path = Path(app.config["LOG_PATH"])  # 来自 Config.LOG_PATH
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "app.log"

    # 日志格式
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 根 logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # 保证能捕获到 DEBUG 以上所有

    # ---- 文件日志 Handler (带轮转) ----
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB 自动轮转
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(app.config["LOG_FILE_LEVEL"])
    root_logger.addHandler(file_handler)

    # ---- 控制台 Handler ----
    if app.config.get("LOG_TO_CONSOLE", False):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(app.config["LOG_CONSOLE_LEVEL"])
        root_logger.addHandler(console_handler)

    # ---- 捕获未处理的异常 ----
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            # 不拦截 Ctrl+C
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        root_logger.error(
            "Uncaught exception",
            exc_info=(exc_type, exc_value, exc_traceback)
        )
    sys.excepthook = handle_exception

    # ---- 捕获 Flask 内部错误 ----
    @app.errorhandler(Exception)
    def log_flask_exception(e):
        app.logger.error("Flask exception", exc_info=e)
        return {"error": str(e)}, 500

    app.logger.info("Logger configured. Logs will be written to %s", log_file)

if __name__ == '__main__':
    app = create_app()
    app.run()