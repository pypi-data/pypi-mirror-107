# -*- coding: utf-8 -*-

"""
配置功能
"""

import configparser

from ..util.singleton import  Singleton

#sdk的配置,先解析好，方便后续调用

#section: sdk_common
class SdkConfig_common(object):
    def __init__(self, config):

        self.port = config.getint('sdk_common', 'port', fallback = 5001)
        self.auth_required = config.getboolean('sdk_common', 'auth_required', fallback=True)
        self.user_id = config.get('sdk_common', 'user_id', fallback = '')
        self.password = config.get('sdk_common', 'password', fallback = '')

        # thread pool
        self.thread_pool_max = config.getint('sdk_common', "thread_pool_max", fallback = 100)
        # log
        self.log_file_max_size = config.getint('sdk_common', 'log_file_max_size', fallback = 100)
        self.log_file_max_number = config.getint('sdk_common', 'log_file_max_number', fallback = 10)

        # 超时时间
        self.connect_timeout = config.getint('sdk_common', 'connect_timeout', fallback = 2)
        self.read_timeout = config.getint('sdk_common', 'read_timeout', fallback = 100)
        self.wait_time = config.getint('sdk_common', 'wait_time', fallback = 100)

        self.service_state_expire = config.getint('sdk_common', 'service_state_expire', fallback = 7200)

#section: sdk_redis
class SdkConfig_redis(object):
    def __init__(self, config):

        # sentinel
        self.sentinel_master = config.get('sdk_redis', 'sentinel_master', fallback = '')
        self.sentinel_nodes = []
        sentinel_nodes_tmp = config.get('sdk_redis', 'sentinel_nodes', fallback = None)
        if sentinel_nodes_tmp:
            node_list = sentinel_nodes_tmp.split(',')
            for node in node_list:
                self.sentinel_nodes.append(tuple(node.split(':')))

        self.host = config.get('sdk_redis', 'host', fallback = '127.0.0.1')
        self.port = config.get('sdk_redis', 'port', fallback = 6379)

        self.db = config.get('sdk_redis', 'db', fallback = 0)
        self.password = config.get('sdk_redis', 'password', fallback = '')

        self.connection_pool_max = config.getint('sdk_redis', 'connection_pool_max', fallback=100)

        # redis 超时时间
        self.socket_connect_timeout = config.getint('sdk_redis', 'socket_connect_timeout', fallback = 2)
        self.socket_timeout = config.getint('sdk_redis', 'socket_timeout', fallback = 2)

#section: sdk_network
class SdkConfig_network(object):
    def __init__(self, config):

        self.network_url = config.get('sdk_network', 'network_url', fallback = '')
        self.network_user_id = config.get('sdk_network', 'network_user_id', fallback = '')
        self.network_password = config.get('sdk_network', 'network_password', fallback = '')
        self.sep_id = config.get('sdk_network', 'sepid', fallback = '')
        self.service_key = config.get('sdk_network', 'service_key', fallback = '')
        self.callevent_subscribe_path = config.get('sdk_network', 'callevent_subscribe_path', fallback = '')
        subscribe_list_tmp = config.get('sdk_network', 'callevent_subscribe_list', fallback = '')
        if subscribe_list_tmp:
            self.callevent_subscribe_list = subscribe_list_tmp.split(',')
        self.callevent_notify_path = config.get('sdk_network', 'callevent_notify_path', fallback = '')
        self.call_control_path = config.get('sdk_network', 'call_control_path', fallback = '')
        self.mock = config.getboolean('sdk_network', 'mock', fallback=False)

# 全部的配置,包括sdk的和业务模块的
@Singleton
class Config(object):

    def __init__(self, file):
        # 配置解析器
        self.__config = configparser.ConfigParser()
        self.__config.read(file, encoding='utf-8')

        # sdk的配置先解析好
        self.__sdkConfig_common = SdkConfig_common(self.__config)
        self.__sdkConfig_redis = SdkConfig_redis(self.__config)
        self.__sdkConfig_network = SdkConfig_network(self.__config)

    def getParser(self):
        return self.__config

    def getSdkConfig_common(self):
        return self.__sdkConfig_common

    def getSdkConfig_redis(self):
        return self.__sdkConfig_redis

    def getSdkConfig_network(self):
        return self.__sdkConfig_network

    #获取字符串键值
    def getstr(self, section, option, fallback=configparser._UNSET):
        # TODO :yxs 这里如果传入fallback会出异常(只需三个参数但传入了四个参数)，奇怪，原因未知，临时把fallback去掉
        #return self.__config.get(section, option, fallback)
        return self.__config.get(section, option)


    # 获取整数键值
    def getint(self, section, option, fallback=configparser._UNSET):
        self.__config.getint(section, option)

    # 获取浮点数键值
    def getfloat(self, section, option, fallback=configparser._UNSET):
        self.__config.getfloat(section, option)


