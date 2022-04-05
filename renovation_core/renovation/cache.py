"""
Base Redis Cache
"""

redis_server = None


class BaseRedisServer:
    def __init__(self, redis_server_instance=None):
        global redis_server
        if not redis_server and redis_server_instance:
            redis_server = redis_server_instance
        if not redis_server:
            raise NotImplementedError

    def get_redis_client(self):
        if redis_server:
            return redis_server
        raise NotImplementedError

    def connected(self):
        raise NotImplementedError

    def get_value(self, *args, **kwargs):
        raise NotImplementedError

    def set_value(self, *args, **kwargs):
        raise NotImplementedError
