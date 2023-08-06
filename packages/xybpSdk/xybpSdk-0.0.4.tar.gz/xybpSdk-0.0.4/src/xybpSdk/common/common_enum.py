from enum import Enum
from flask import Response


# 呼叫事件类型
class CallEventEnum(Enum):

    BEGIN = 'Begin'
    ANSWER = 'Answer'
    OTHER = ('Busy', 'Not Reachable', 'No Answer', 'Abandon', 'Release', 'Route Failure', 'Exception')


# 主被叫业务状态
class ServiceStateEnum(Enum):
    OVER = 0
    BEGIN = 1


# API ID
class APIIDEnum(Enum):
    # 呼叫事件订阅接口（平台级）
    CALL_EVENT_PLATFORM_SUBSCRIPTION_API_ID = '60001'

    # 呼叫控制接口
    CALL_CONTROL_API_ID = '60007'


# 呼叫控制消息类型
class CallControlEnum(Enum):

    CONTINUE = 'Continue'
    END_CALL = 'EndCall'
    PLAY = 'Play'
    PLAY_COLLECT = 'PlayAndCollect'

# 呼叫流程
class CallProcessEnum(Enum):

    # 主叫流程
    MO = 'MO'
    # 被叫流程
    MT = 'MT'
    # 前转流程
    CF = 'CF'

# 通知模式
class NotificationModeEnum(Enum):
    NOTIFICATION_MODE = 'Notify'
    BLOCK_MODE = 'Block'

# 响应错误
class ResponseResultEnum(Enum):

    OK = Response(None, 200, headers={'Content-Type': 'application/json;charset=UTF-8'})

    AUTH_FAILED = {'code': '0000201', 'description': '请求鉴权失败'}, 403
    INVALID_REQUEST_PARAMETER = {'code': '0000002', 'description': '请求参数无效'}, 400

