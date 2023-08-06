import requests
import requests_mock

from ..config.config import Config

# 封装http请求

class HttpClient(object):

    """Http request client

    Only post requests are currently supported
    """

    '''
    yxs 注释，目前没用
    @staticmethod
    def post(url, data, auth=None, timeout=None):
        """Send Post request

        Args:
            url: URL
            data: json string
            auth: HTTP_BASIC_AUTH {'user_id': Aladdin, 'password': 'open sesame'}
            timeout: Tuple data type. For example:：(connect_timeout, read_timeout)

        Returns:
            Response body data

        Raises:
            Exception: An exception occurred request failed or error.
        """
        http_basic_auth = None

        # 如果需要鉴权
        if auth:
            http_basic_auth = requests.auth.HTTPBasicAuth(auth['user_id'], auth['password'])

        # 参数为空, 从配置中获取
        if not timeout:
            timeout = (config.getSdkConfig_common().connect_timeout, config.getSdkConfig_common().read_timeout)

        res = requests.post(url, data, headers={'Content-Type': 'application/json;charset=UTF-8'},
                            auth=http_basic_auth, timeout=timeout)

        # 通过status_code判断请求结果是否正确
        if res.status_code == 200:
            if res.text == '':
                return {}
            return res.json() or {}

        raise Exception('request error，url: {}，status_code: {}，failed reason：{}'.format(url, str(res.status_code), str(res.reason)))
    '''

    # 向能力网元发送post请求
    @staticmethod
    def post_to_network(url, data, auth=None, timeout=None):

        http_basic_auth = None

        config = Config()

        try:
            if auth:
                # yxs 我的理解：HTTPBasicAuth会自动实现头部的Authorization:Basic <base64 encoded (user-pass)>
                http_basic_auth = requests.auth.HTTPBasicAuth(auth['userid'], auth['password'])
            if not timeout:
                timeout = (config.getSdkConfig_common().connect_timeout, config.getSdkConfig_common().read_timeout)

            # 真实发送
            if False == config.getSdkConfig_network().mock:
                res = requests.post(url, data, headers={'Content-Type': 'application/json;charset=UTF-8'},
                                    auth=http_basic_auth, timeout=timeout)
            # mock发送
            else:

                with requests_mock.Mocker() as mock:
                    mock.post(url, json={"code": "0000000"})    # 成功应答不需要data,这里随便填
                    res = requests.post(url, data, headers={'Content-Type': 'application/json;charset=UTF-8'}, auth=http_basic_auth, timeout=timeout)
        except Exception as e:
            raise e
        else:
            return res
