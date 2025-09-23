# -*- coding: utf-8 -*-
# gunicornconf.py

# 绑定的 ip:port
bind = ["0.0.0.0:5000"]

# 使用 eventlet 协程 worker
worker_class = "eventlet"

# worker 进程数（CPU 核数不多时 SSE 场景 1~2 个即可）
workers = 1

# 单个 worker 内最大并发连接数（eventlet/gevent 专用）
worker_connections = 20

# 其余常用可选配置
keepalive = 2
max_requests = 0           # 0 表示不限制，SSE 连接需要长寿命
preload_app = False         # 预加载代码，节省内存
accesslog = '/var/log/gunicorn_acess.log'
errorlog = '/var/log/gunicorn_error.log'
# daemon = True  # 以守护进程模式运行（后台运行）