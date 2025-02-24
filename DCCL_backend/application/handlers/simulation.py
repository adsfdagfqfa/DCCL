from datetime import datetime
from .base import routes

@routes.route("/today",methods=['GET'])
def simulation():
    return datetime.today().strftime('%Y-%m-%d %H:%M:%S')