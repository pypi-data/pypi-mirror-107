# -*- coding: utf-8 -*-

import redis
from redis.sentinel import Sentinel

"""
redis封装
"""


class RedisHelper:
    def __init__(self, sdkConfig):
        self.__sdkConfig = sdkConfig

        self.sentinel = None
        self.my_redis = None

        socket_timeout = sdkConfig.socket_timeout
        socket_connect_timeout = sdkConfig.socket_connect_timeout

        # 单实例
        if sdkConfig.sentinel_nodes:
            self.sentinel = Sentinel(sdkConfig.sentinel_nodes, socket_timeout=socket_timeout,
                                     socket_connect_timeout=socket_connect_timeout, decode_responses=True)
        else:
            # 创建连接池
            pool = redis.ConnectionPool(host=sdkConfig.host,
                                        port=sdkConfig.port,
                                        db=sdkConfig.db,
                                        password=sdkConfig.password,
                                        decode_responses=True, max_connections=sdkConfig.connection_pool_max,
                                        socket_connect_timeout=socket_connect_timeout, socket_timeout=socket_timeout)
            self.my_redis = redis.StrictRedis(connection_pool=pool)

    def get_redis(self):
        # 单实例
        if not self.my_redis:
            # sentinel
            self.my_redis = self.sentinel.master_for(self.__sdkConfig.sentinel_master,
                                                     db=self.__sdkConfig.db,
                                                     password=self.__sdkConfig.password,
                                                     socket_timeout=1)

        return self.my_redis


redisHelper = None


def init_redis(sdkConfig):
    global redisHelper
    redisHelper = RedisHelper(sdkConfig)



