import jwt
import datetime
import application.config as config
from application.extensions import redis_client
def generate_jwt_token(uuid, algorithm='HS256'):

    payload = {
        'uuid': uuid,  # User ID
        # 'exp': datetime.datetime.now() + datetime.timedelta(hours=1),  # Token expiration time
        'iat': datetime.datetime.utcnow(),  # Token issuance time
    }
   
    secret_key = config.Config.SECRET_KEY
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token

def verify_jwt_token(token):
    # 验证现有Token
    try:
        #设置时间容错
        leeway = datetime.timedelta(minutes=5)
        payload = jwt.decode(token, config.Config.SECRET_KEY, algorithms='HS256', leeway = leeway)
        uuid = payload['uuid']
        # 检查Redis是否存在用户记录（可选）
        if not redis_client.exists(uuid):
            # 数据过期
            return False
        return True
    except jwt.ExpiredSignatureError:
        # Token过期
        print("Token has expired")
        return False
    except jwt.InvalidTokenError as e:
        # 非法Token
        print(f"Invalid token: {e}")
        return False
    
#从token中提取uuid
def get_uuid_from_token(token):
    leeway = datetime.timedelta(minutes=5)
    payload = jwt.decode(token, config.Config.SECRET_KEY, algorithms='HS256', leeway = leeway)
    uuid = payload['uuid']
    return uuid
      
   