import json
import time
from loguru import logger

from ..common.common_enum import *
from ..config.config import Config
from ..util.requests_utils import HttpClient
from ..util.singleton import Singleton

"""
能力网元业务处理
"""

@Singleton
class NetworkService:

    def __init__(self):
        self.__Config = Config()

    # 向能力网元发送呼叫控制消息
    # action: Continue | EndCall | Play | PlayAndCollect
    # call_identifier: 呼叫ID
    # data: post data
    def send_call_control_msg(self, action, call_identifier, data=None):

        # 组装 url， 参数，auth
        url, auth = self.build_call_control_request(call_identifier)

        logger.info("send [call_control_msg] [action：{}，call_identifier: {}] to network [{}], post data: {}, auth: {}",
                    action, call_identifier, url, data, auth)

        # 发送 Continue 消息

        try:
            res = HttpClient.post_to_network(url, json.dumps(data), auth=auth)
        except Exception as e:
            logger.error('send req [call_control_msg] [action：{}, call_identifier: {} exception, err msg: {}', action, call_identifier, e)
        else:
            if res.status_code == 200:
                logger.info('send req [call_control_msg] [action：{}, call_identifier: {} successfully', action, call_identifier)
            else:
                logger.error('send req [call_control_msg] [action：{}, call_identifier: {} fail, status_code={}', action, call_identifier, res.status_code)

    # 组装请求信息 url ，param， auth
    def build_call_control_request(self, call_identifier):
        config_network = self.__Config.getSdkConfig_network()

        # 拼接 url
        url = config_network.network_url + '/' + config_network.call_control_path
        url = url.format(call_identifier)

        # 获取 auth
        user_id = config_network.network_user_id
        password = config_network.network_password
        auth = {'userid': user_id, 'password': password}

        return url, auth

    # 呼叫事件订阅(平台级)
    # ps: 关于重复订阅的返回结果(基于实际测试情况)
    # 重复订阅分两种情况: 1. 两次订阅的事件一样 2. 两次订阅的事件部分相同
    # 情况 1. 返回结果是 400
    # 情况 2. 返回结果是 409
    def subscribe_platform_level_call_events(self):
        # 待订阅事件列表
        all_events = self.__Config.getSdkConfig_network().callevent_subscribe_list

        # Begin事件的notificationmode需要为Block,其他事件的notificationmode需要为Notify，因此分成两个列表
        begin_events = []
        other_events = []
        for event in all_events:
            if 'Begin' == event:
                begin_events.append(event)
            else:
                other_events.append(event)


        sub_result = {'Begin': False, 'Other': False}
        if not begin_events:
            sub_result['Begin'] = True
        if not other_events:
            sub_result['Other'] = True

        # 直到所有事件都订阅成功
        while True:
            # Begin 事件未订阅成功
            if not sub_result.get('Begin'):
                # 发起一次订阅
                begin_subscribe_result = self.call_events_subscribe(['Begin'], 'Block')
                if begin_subscribe_result in (200, 400, 409):
                    sub_result['Begin'] = True

            time.sleep(self.__Config.getSdkConfig_common().wait_time)

            # 其他事件未订阅成功
            if not sub_result.get('Other'):
                # 发起一次订阅
                result = self.call_events_subscribe(other_events, 'Notify')
                if result in (200, 400, 409):
                    sub_result['Other'] = True

            # 事件全部订阅成功
            if sub_result.get('Begin') and sub_result.get('Other'):
                logger.info('all call events subscribed successfully.')
                break
            else:
                logger.info('not all events were successfully subscribed[{}]. wait 3 seconds!', sub_result)
                time.sleep(self.__Config.getSdkConfig_common().wait_time)

    # 事件订阅
    def call_events_subscribe(self, call_events, notification_mode):

        # 请求 url
        url = self.__Config.getSdkConfig_network().network_url + self.__Config.getSdkConfig_network().callevent_subscribe_path
        auth = {'userid': self.__Config.getSdkConfig_network().network_user_id, 'password': self.__Config.getSdkConfig_network().network_password}

        # 封装请求参数
        params = {
            'sepid': self.__Config.getSdkConfig_network().sep_id,
            'APIID': APIIDEnum.CALL_EVENT_PLATFORM_SUBSCRIPTION_API_ID.value,
            'ServiceKey': [self.__Config.getSdkConfig_network().service_key],
            'events': call_events,
            'notificationmode': notification_mode
        }

        logger.info('send {} Call event subscription，params: {}', call_events, params)

        try:
            res = HttpClient.post_to_network(url, json.dumps(params), auth)
        except Exception as e:
            logger.error('{} Call event subscription exception, err msg: {}', call_events, e)
            return -1
        else:
            if res.status_code == 200:
                logger.info('{} Call event subscription successfully', call_events)
            elif res.status_code in (400, 409):
                logger.warning('{} Call event Already subscribed，res: {}', call_events, str(res))
            else:
                logger.error('{} Call event subscription error, res: {}', call_events, str(res))
            return res.status_code

