"""
Main client class

@author: Acellam Guy
"""
import json
try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

import requests
from requests import Request, Session
from requests._internal_utils import to_native_string
from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth


from .config import PaylenseConfig
from .errors import APIError
from .utils import requests_retry_session


class Response:

    def __init__(self, body, code, headers):
        self.body = body
        self.code = code
        self.headers = headers
        self.data = body


class ClientInterface():
    def getTransactionStatus(self):
        raise NotImplementedError


class Client(ClientInterface):
    def getTransactionStatus(self):
        return super(Client, self).getTransactionStatus()


class Paylense(ClientInterface, object):

    def __init__(
            self,
            config,
            ** kwargs):
        super(Paylense, self).__init__(**kwargs)
        self._session = Session()
        self._config = PaylenseConfig(config)

    @property
    def config(self):
        return self._config

    def request(self, method, url, post_data=None):
        headers = {
            "Content-Type": "application/json",
            "APP-ID": self.config.app_id
        }
        request = Request(
            method,
            url,
            data=json.dumps(post_data),
            headers=headers,
            auth=HTTPBasicAuth(
                self.config.username,
                self.config.password))

        prepped = self._session.prepare_request(request)

        resp = requests_retry_session(sesssion=self._session).send(prepped,
                                                                   verify=False
                                                                   )
        return self.interpret_response(resp)

    def interpret_response(self, resp):
        rcode = resp.status_code
        rheaders = resp.headers
        print(resp)

        try:
            rbody = resp.json()
        except JSONDecodeError:
            rbody = resp.text
            resp = Response(rbody, rcode, rheaders)

        if not (200 <= rcode < 300):
            self.handle_error_response(rbody, rcode, resp.text, rheaders)

        return resp

    def handle_error_response(self, rbody, rcode, resp, rheaders):

        raise APIError(
            "Invalid response object from API: {0} (HTTP response code "
            "was {1})".format(rbody, rcode),
            rbody, rcode, resp)

    def request_headers(self, api_key, method):
        headers = {}

        return headers

    def getTransactionStatus(
            self,
            transaction_id,
            url,
            ** kwargs):

        _url = self.config.baseUrl + url + transaction_id
        print(_url)
        res = self.request("GET", _url)
        return res.json()

    def close(self):
        if self._session is not None:
            print("closing!")
            self._session.close()
