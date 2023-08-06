import base64
from loguru import logger
from ..config import config
from ..config.config import Config


class CommonService:

    def __init__(self):
        pass

    # basic 鉴权
    # 正常参数格式： Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==
    def basic_auth(self, authorization):
        # 判断authorization是否为空
        if authorization is None or authorization == '':
            return False

        # 按照空格拆分
        authorizations = authorization.split(' ')
        if len(authorizations) != 2:
            return False

        authorization_basic = authorizations[0]
        authorization_digest = authorizations[1]

        if authorization_basic != 'Basic':
            return False

        # base64 解码
        try:
            decode_bytes = base64.b64decode(authorization_digest)
            decode_str = str(decode_bytes, 'utf-8')
        except Exception as e:
            logger.error('http basic decode failed, error msg: {}', e)
            return False

        # 获取用户名和密码
        user_info = decode_str.split(':')

        if len(user_info) != 2:
            return False

        user_id = user_info[0]
        password = user_info[1]

        # 获取配置文件中用户名和密码
        config = Config()
        config_user_id = config.getSdkConfig_common().user_id
        config_password = config.getSdkConfig_common().password

        #两者相等
        if user_id == config_user_id and password == config_password:
            return True

        return False






