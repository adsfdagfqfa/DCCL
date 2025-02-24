from datetime import datetime
from .base import routes

@routes.route("/test",methods=['GET'])
def test():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
