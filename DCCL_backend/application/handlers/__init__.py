
from .base import routes
from handlers import aperture
from handlers import simulation
from handlers import *
@routes.route('/test1',methods=['GET'])
def t():
    print(1)
    return '1'

def init_app(app):
    
    print("路由注册")
    app.register_blueprint(routes)
    
