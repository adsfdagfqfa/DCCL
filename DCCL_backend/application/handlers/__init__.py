
from .base import routes

from application.handlers import simulation
from application.handlers import *
@routes.route('/test1',methods=['GET'])
def t():
    print(1)
    return '1'

def init_app(app):
    
    print("路由注册")
    app.register_blueprint(routes)
    
