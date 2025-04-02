from application.extensions import redis_client

def get_redis_data(id):
    data = redis_client.get(id)
    if data:
        return data
    return None


def set_redis_data(id,data):
    redis_client.set(id, data)