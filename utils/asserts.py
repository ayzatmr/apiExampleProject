import json

import allure
from hamcrest import assert_that, equal_to

from utils.files_reader import app_config

loadtest_mode = app_config()['loadtest']


@allure.step("Check that: {2}")
def check_that(actual, matcher, message=""):
    assert_that(actual, matcher, message)


def is_json(obj):
    try:
        obj.json()
    except ValueError:
        return False
    return True


class CustomAssert:
    @allure.step("Check request status: actual = {1}, expected = {2}")
    def log_assert_status(self, logger, actual, expected):
        if expected != actual.status_code:
            if is_json(actual):
                logger.error(json.dumps(actual.json(), indent=4, sort_keys=True, ensure_ascii=False))
                if loadtest_mode:
                    actual.failure(actual.json())
                assert_that(actual.status_code, equal_to(expected))
            else:
                if loadtest_mode:
                    actual.failure(actual.json())
                assert_that(actual.status_code, equal_to(expected))
        else:
            if is_json(actual):
                logger.info("RESPONSE = " + json.dumps(actual.json(), indent=4, sort_keys=True, ensure_ascii=False))
                if loadtest_mode:
                    actual.success()
                assert_that(actual.status_code, equal_to(expected))
            else:
                if loadtest_mode:
                    actual.success()
                assert_that(actual.status_code, equal_to(expected))
