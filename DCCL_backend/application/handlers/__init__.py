
from .base import routes
import logging
from application.handlers import simulation,result
from application.handlers import *
logger= logging.getLogger(__name__)
@routes.route('/test1',methods=['GET'])
def t():
    return '1'

def init_app(app):
    
    logger.info("路由注册")
    app.register_blueprint(routes)
    
