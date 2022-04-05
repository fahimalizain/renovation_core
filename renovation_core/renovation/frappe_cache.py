"""
Frappe Uses different caching strategies.. Let me attempt to list them
1. Process level cache ie global variables stored at the worker level.
2. local (werkzerug.locals) for request level cache.
3. Redis servers. In particular frappe uses 3
   => frappe cache ie the most commonly used one by web workers
   => socketio ie for real time communication
   => queue ie to maintain background job queues.

Besides the above frappe caching methods the following caching is also observed..
4. One more layer of caching was introduced with the usage of dataloaders

"""
import frappe
from renovation.cache import BaseRedisServer

"""
This is frappe cache as mentioned in above comment
"""


class FrappeCache(BaseRedisServer):
    def __init__(self):
        cache = frappe.cache()
        super(FrappeCache, self).__init__(cache)

    def connected(self):
        return self.get_redis_client().connected()

    def get_value(self, *args, **kwargs):
        raise self.get_redis_client().get_value(*args, **kwargs)

    def set_value(self, *args, **kwargs):
        raise self.get_redis_client().set_value(*args, **kwargs)
