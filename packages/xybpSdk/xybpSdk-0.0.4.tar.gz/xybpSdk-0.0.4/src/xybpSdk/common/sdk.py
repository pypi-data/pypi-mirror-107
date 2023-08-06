
from flask import Flask
from flask_restful import Resource, Api
from api import *
from ..config.config import Config

from ..service import NetworkService
from ..util.singleton import  Singleton
from ..util import log, redis_utils, thread_utils

# Flask框架
app = Flask(__name__)
api = Api(app)

# 演示用Flask路由
class HelloWorld(Resource):
    def get(self):
        return 'hello world'

api.add_resource(HelloWorld, '/')


# sdk入口类
@Singleton
class Sdk(object):
    def __init__(self):
        # 是否已初始化
        self.__is_open = False
        # 配置
        self.__config = None
        # 能力网元服务
        self.__networkService = None

    # 初始化
    def open(self, cfgFile, callEventResource):
        if True  == self.__is_open:
            return

        #配置初始化
        self.__config = Config(cfgFile)

        # 日志初始化
        log.init_log(self.__config.getSdkConfig_common())

        # redis初始化
        redis_utils.init_redis(self.__config.getSdkConfig_redis())

        # 线程池初始化
        thread_utils.init_thread_pool_executor(self.__config.getSdkConfig_common().thread_pool_max, 'Event_Thread')

        # 能力网元服务初始化
        self.__networkService = NetworkService()

        # 注册能力网元通知回调函数
        api.add_resource(callEventResource, self.__config.getSdkConfig_network().callevent_notify_path)

        self.__is_open = True

    # 运行
    def run(self):
        if False == self.__is_open:
            return

        # 向能力网元订阅所需事件
        NetworkService().subscribe_platform_level_call_events()

        # web server启动，会一直阻塞在此
        app.run(host='0.0.0.0', port=self.__config.getSdkConfig_common().port, debug=False, use_reloader=False, threaded=True)

    # 关闭
    def close(self):
        if True == self.__is_open:
            #TODO 其它关闭操作
            
            self.is__open = False

    # 获取配置
    def getConfig(self):
        return self.__config