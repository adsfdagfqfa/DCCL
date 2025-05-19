workers = 1
bind = '0.0.0.0:5000'
timeout = 1000
accesslog = '/var/log/gunicorn_acess.log'
errorlog = '/var/log/gunicorn_error.log'
# daemon = True  # 以守护进程模式运行（后台运行）