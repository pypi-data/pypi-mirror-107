import json
from random import randint
from requests import Session
from requests.exceptions import ConnectionError
from json.decoder import JSONDecodeError
from .errors import OperationError, ServiceError, ParameterError


class ResponseObject(object):
    def __init__(self, response):

        self.status = response['status']
        self.success = response['success']
        self.response_data = response['response']
        self.response_headers = response['headers']
        self.response_url = response['response_url']

        self.encoded = None
        if 'encoded' in response:
            self.encoded = response['encoded']

        # Legacy options
        self.text = self.response_data
        self.status_code = self.status

    def json(self):
        return json.loads(self.response_data)


class CFService(object):
    def __init__(self, host: str, headers=None, timeout=None):
        self.host = host
        self.timeout = timeout
        self.headers = headers
        self.session = Session()

    def __get_proxy(self, proxy_string: str) -> str:

        components = proxy_string.replace('\r', '').split(':')

        [host, port, user, password] = components

        parsed = f'{host}:{port}'

        if user is not None and password is not None:

            parsed = f'{user}:{password}@{host}:{port}'

        return f'http://{parsed}'

    def __simplify_proxy(self, proxy_dict: dict = {}) -> str:

        if 'http' in proxy_dict:
            return proxy_dict['http']

        if 'https' in proxy_dict:
            https_proxy = proxy_dict['https']
            return f"{https_proxy}".replace("https://", "http://")

    def get(self, url: str, proxy: str = None, proxies: dict = None, headers: dict = None, params: any = None, solve: bool = False, timeout: int = None) -> object:

        try:

            seed = 300 + randint(1, 1000)

            parsed = None

            if proxy is not None:
                parsed = self.__get_proxy(proxy)

            if proxies is not None:
                parsed = self.__simplify_proxy(proxies)

            if parsed is None:
                raise Exception('No proxy provided')

            if headers is None:
                if self.headers is None:
                    headers = {}
                else:
                    headers = self.headers

            if timeout is None:
                timeout = self.timeout

            json = {
                "url": url,
                "solve": solve,
                "params": params,
                "headers": headers,
                "timeout": timeout,
                "proxy": {
                    "parsed": parsed
                },
            }

            target = f"{self.host}/fetch"

            params = {
                "seed": seed
            }

            agent_headers = {
                'User-Agent': 'cfs-support-router'
            }

            res = self.session.post(
                url=target, headers=agent_headers, json=json, params=params)

            if res.status_code == 502:
                raise ServiceError('CFS - Bad gateway')

            response = res.json()

            if not response['success']:
                error = response['error']

                if res.status_code == 401:
                    raise OperationError(error)

                if res.status_code == 403:
                    raise ParameterError(error)

                if res.status_code == 500:
                    error = response['error']
                    raise ServiceError(error)

                raise OperationError(error)

            response_object = ResponseObject(response)

            if not response_object.success:
                raise OperationError('Request failed')

            return response_object

        except JSONDecodeError:
            raise OperationError('JSON: Invalid Response')

        except ConnectionError:
            raise OperationError('Unable to connect to CF Service')

    def post(self, url: str, proxy: str = None, proxies: dict = None, params: any = None, body: dict = {}, headers: dict = None, solve: bool = False, timeout: int = None) -> object:

        try:
            seed = 300 + randint(1, 1000)

            parsed = None

            if proxy is not None:
                parsed = self.__get_proxy(proxy)

            if proxies is not None:
                parsed = self.__simplify_proxy(proxies)

            if parsed is None:
                raise Exception('No proxy provided')

            if headers is None:
                if self.headers is None:
                    headers = {}
                else:
                    headers = self.headers

            if timeout is None:
                timeout = self.timeout

            json = {
                "url": url,
                "body": body,
                "solve": solve,
                "params": params,
                "timeout": timeout,
                "proxy": parsed,
                "headers": headers,
            }

            target = f"{self.host}/submit"

            params = {
                "seed": seed
            }

            agent_headers = {
                'User-Agent': 'cfs-support-router'
            }

            res = self.session.post(
                url=target, headers=agent_headers, json=json, params=params)

            if res.status_code == 502:
                raise ServiceError('CFS - Bad gateway')

            response = res.json()

            if not response['success']:
                error = response['error']

                if res.status_code == 401:
                    raise OperationError(error)

                if res.status_code == 403:
                    raise ParameterError(error)

                if res.status_code == 500:
                    error = response['error']
                    raise ServiceError(error)

                raise OperationError(error)

            response_object = ResponseObject(response)

            if not response_object.success:
                raise OperationError('Request failed')

            return response_object

        except JSONDecodeError:
            raise OperationError('JSON: Invalid Response')

        except ConnectionError:
            raise OperationError('Unable to connect to CF Service')
