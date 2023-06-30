from locust import TaskSet, HttpUser, between, events

from base import logger
from utils.files_reader import get_creds_from_file


@events.quitting.add_listener
def _(environment, **kwargs):
    if environment.stats.total.fail_ratio > 0.1:
        logger.error("Test failed due to failure ratio > 10%")
        environment.process_exit_code = 1
    elif environment.stats.total.avg_response_time > 2000:
        logger.error("Test failed due to average response time ratio > 2000 ms")
        environment.process_exit_code = 1
    elif environment.stats.total.get_response_time_percentile(0.95) > 3000:
        logger.error("Test failed due to 95th percentile response time > 3000 ms")
        environment.process_exit_code = 1
    else:
        environment.process_exit_code = 0


class BaseTaskSet(TaskSet):

    def __init__(self, parent, path) -> None:
        super().__init__(parent)
        self.path = get_creds_from_file(path)

    def on_start(self):
        self.email = 'Not_exist'
        self.password = 'Not_exist'
        if len(self.path) > 0:
            self.email, self.password = self.path.pop()


"""
set the base load config
before start change value in loadtest in application.yaml
"""


class BaseHttpUser(HttpUser):
    wait_time = between(0, 1)
    tasks = []
    host = '/'
    abstract = True
