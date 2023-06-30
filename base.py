import json
from functools import lru_cache

import allure
import locust
from locust import HttpUser, task
from locust.env import Environment
from schematics.validate import validate

from logger.logger import prepared_logger

__all__ = [
    'BaseApiClient',
    'BaseSteps',
    'validate_response'
]

from utils.asserts import CustomAssert

from utils.auth import AdminAuth, RootAuth

from utils.files_reader import app_config
from utils.helper import my_session, join_url_paths

configuration = app_config()
strict_validation = configuration['strict_validation']
loadtest_mode = configuration['loadtest']
logger = prepared_logger()


class BaseSteps:
    def __init__(self, client):
        self._client = client
        self.config = configuration
        self.logger = logger


class BaseApiClient(HttpUser):
    """Base API Client."""

    def __init__(self, api_type, *args, **kwargs):
        """For each type of API need different token"""
        super().__init__(Environment(events=locust.events, catch_exceptions=True), *args, **kwargs)
        self._api_type = api_type

    @property
    @lru_cache(maxsize=None)
    def _auth_type(self):
        """Get custom auth module.
        Returns:
            object: AuthBase extension.
        """
        if 'admin' == self._api_type:
            return AdminAuth(None, None)
        elif 'root' == self._api_type:
            return RootAuth()
        else:
            return None

    @property
    def _url(self):
        """Get base_url for each client type.
        Returns:
            object: url.
        """
        if 'admin' == self._api_type:
            return configuration['url']['admin']
        elif 'root' == self._api_type:
            return configuration['url']['root']
        else:
            return None

    """"Workaround for HttpUser class"""
    host = '/'

    @property
    def session(self):
        if loadtest_mode:
            return self.client
        else:
            return my_session()

    @task
    def _post(self, url=None, headers=None, data=None, json=None, auth=None, **kwgs):
        """POST request to API."""
        auth = auth or self._auth_type
        headers = headers or configuration['headers']['common']
        url = (lambda x: self._url if x is None else join_url_paths(self._url, url))(url)
        if loadtest_mode:
            return self.session.post(url, headers=headers, data=data, json=json, auth=auth, catch_response=True, **kwgs)
        else:
            return self.session.post(url, headers=headers, data=data, json=json, auth=auth, **kwgs)

    @task
    def _get(self, url=None, headers=None, params=None, auth=None, **kwgs):
        """Get request to API."""
        auth = auth or self._auth_type
        headers = headers or {'Accept-Language': 'en'}
        url = (lambda x: self._url if x is None else join_url_paths(self._url, url))(url)
        if loadtest_mode:
            return self.session.get(url, headers=headers, params=params, auth=auth, catch_response=True, **kwgs)
        else:
            return self.session.get(url, headers=headers, params=params, auth=auth, **kwgs)

    @task
    def _delete(self, url=None, headers=None, auth=None, **kwgs):
        """DELETE request to API."""
        auth = auth or self._auth_type
        headers = headers or configuration['headers']['common']
        url = (lambda x: self._url if x is None else join_url_paths(self._url, url))(url)
        if loadtest_mode:
            return self.session.delete(url, headers=headers, auth=auth, catch_response=True, **kwgs)
        else:
            return self.session.delete(url, headers=headers, auth=auth, **kwgs)

    @task
    def _put(self, url=None, headers=None, data=None, auth=None, **kwgs):
        """PUT request to API."""
        auth = auth or self._auth_type
        headers = headers or configuration['headers']['common']
        url = (lambda x: self._url if x is None else join_url_paths(self._url, url))(url)
        if loadtest_mode:
            return self.session.put(url, headers=headers, data=data, auth=auth, catch_response=True, **kwgs)
        else:
            return self.session.put(url, headers=headers, data=data, auth=auth, **kwgs)

    @task
    def _patch(self, url=None, headers=None, data=None, auth=None, **kwgs):
        """PATCH request to API."""
        auth = auth or self._auth_type
        headers = headers or configuration['headers']['common']
        url = (lambda x: self._url if x is None else join_url_paths(self._url, url))(url)
        if loadtest_mode:
            return self.session.patch(url, headers=headers, data=data, auth=auth, catch_response=True, **kwgs)
        else:
            return self.session.patch(url, headers=headers, data=data, auth=auth, **kwgs)


'''
Magic method that:
    - log post data 
    - log request_id
    - validate response
    - log response and status
    - generate allure report headings
'''


def validate_response(http_status, schema=None):
    def inner_decorator(func):
        def wrapper(*args, **kwargs):
            with allure.step(str(func.__name__)):
                strict = strict_validation
                logger.info(f"Step: {func.__name__} started")
                with func(*args, **kwargs) as response:
                    logger.info(f"request_id = {response.headers.get('x-request-id')}")
                    _log_command(*args, **kwargs)
                    CustomAssert().log_assert_status(logger, response, http_status)
                    if schema:
                        if isinstance(response.json(), list):
                            for content in response.json():
                                validate(schema, content, strict=strict)
                        else:
                            validate(schema, response.json(), strict=strict)
                    logger.info(f"Step: {func.__name__} done")
                    return response

        return wrapper

    return inner_decorator


def _log_command(*args, **kwargs):
    if kwargs.get('command'):
        logger.info('command: ' + json.dumps(kwargs.get('command'), indent=4, sort_keys=True, ensure_ascii=False))
    else:
        for arg in args:
            if isinstance(arg, dict):
                logger.info('command: ' + json.dumps(arg, indent=4, sort_keys=True, ensure_ascii=False))
