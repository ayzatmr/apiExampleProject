import logging
import time

from utils.asserts import check_that

logger = logging.getLogger(__name__)

"""Method allows to wait specific value in rest response and make polling during some time"""


def implicit_wait(
        obj, keys_array, check_value, start_waiting_time, stop_waiting_time, polling_time, func=None, *args, **kwargs):
    time.sleep(start_waiting_time)
    response = None
    while start_waiting_time <= stop_waiting_time:
        try:
            response = obj(*args, **kwargs)
            if keys_array:
                content = response.json()
                try:
                    for key in keys_array:
                        try:
                            content = content[key]
                        except KeyError:
                            time.sleep(polling_time)
                            start_waiting_time += polling_time
                    if func:
                        try:
                            check_that(content, func(check_value), "")
                            logger.info(f"Waiting time is {start_waiting_time} seconds")
                            return response
                        except AssertionError:
                            time.sleep(polling_time)
                            start_waiting_time += polling_time
                    elif content == check_value:
                        logger.info(f"Waiting time is {start_waiting_time} seconds")
                        return response
                    else:
                        time.sleep(polling_time)
                        start_waiting_time += polling_time
                except IndexError:
                    time.sleep(polling_time)
                    start_waiting_time += polling_time
            else:
                logger.info(f"Waiting time is {start_waiting_time} seconds")
                return response
        except AssertionError:
            time.sleep(polling_time)
            start_waiting_time += polling_time
    logger.info(f"Waiting time is {start_waiting_time} seconds")
    return response


def implicit_wait_in_list(obj, before_keys_array, inner_keys_array, check_value, start_waiting_time,
                          stop_waiting_time, polling_time, *args, **kwargs):
    time.sleep(start_waiting_time)
    response = None
    while start_waiting_time <= stop_waiting_time:
        response = obj(*args, **kwargs)
        content = response.json()
        try:
            for key in before_keys_array:
                try:
                    content = content[key]
                except KeyError:
                    time.sleep(polling_time)
                    start_waiting_time += polling_time
            for content_item in content:
                check_content = content_item
                for item_key in inner_keys_array:
                    try:
                        check_content = check_content[item_key]
                    except KeyError:
                        break
                if check_content == check_value:
                    logger.info(f"Waiting time is {start_waiting_time} seconds")
                    return content_item
            else:
                time.sleep(polling_time)
                start_waiting_time += polling_time
        except IndexError:
            time.sleep(polling_time)
            start_waiting_time += polling_time
    logger.info(f"Waiting time is {start_waiting_time} seconds")
    return response
