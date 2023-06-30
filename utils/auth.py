import logging

from requests.auth import AuthBase

from constants.request_constants import AUTH
from utils.decorator import func_once
from utils.files_reader import app_config
from utils.helper import my_session

config = app_config()
header = config['headers']['common']['content-type']


@func_once
def get_token(email, password, url):
    response = my_session().post(
        url=url + AUTH,
        data={"email": email, "password": password},
        headers=config['headers']['auth'])
    return response


class AdminAuth(AuthBase):
    def __init__(self, email, password):
        self.logger = logging.getLogger(__name__)
        self.email = email
        self.password = password
        self.url = config['url']['admin']

    def __call__(self, r):
        response = get_token(
            email=self.email,
            password=self.password,
            url=self.url)
        self.logger.info("admin:" + str(response.json()))
        r.headers['Authorization'] = 'Bearer ' + response.json().get("token", "invalid")
        r.headers["Accept"] = config['headers']['common']['content-type']
        return r


class RootAuth(AuthBase):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def __call__(self, r):
        token = config['credentials']['root']['token']
        self.logger.info("root token = " + token)
        r.headers['X-Root-Secret'] = token
        r.headers["Accept"] = header
        return r
