import pytest

from AdminApi.steps.admin_branch_steps import BranchSteps
from base import BaseApiClient
from enums.application_type import Application


# needs to be like that to adapt the code for load tests
def branch_steps_method():
    return BranchSteps(BaseApiClient(Application.Admin.value))


@pytest.fixture(scope="session")
def branch_steps():
    return branch_steps_method()
