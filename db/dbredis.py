from flask_redis import FlaskRedis
import  threading

class RedisMgr:
    __store = None
    def __new__(clz, flask_app):
          #RLock對象 
        try:
            if not RedisMgr.__store:
                RedisMgr.__store = FlaskRedis(flask_app)
        finally:
            pass
        return RedisMgr.__store

    @staticmethod    
    def initial(flask_app):
        RedisMgr(flask_app)
        return RedisMgr.__store

    @staticmethod    
    def get_store():
        if(RedisMgr.__store is None):
            raise ValueError("FlaskRedis store is not initialize....")
        return RedisMgr.__store

import redis

rd_pool = redis.ConnectionPool(
    host='localhost', password='pwd123456', port=6379, decode_responses=True)
rd_base = redis.Redis(connection_pool=rd_pool)
