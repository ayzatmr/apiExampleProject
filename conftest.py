import random

import pytest

from AdminApi.models.commands.branch import Branch
from AdminApi.models.commands.company import Company, Admin
from utils.files_reader import read_plugin_names, get_profile

pytest_plugins = read_plugin_names()


# create one company for
@pytest.fixture(scope="class")
def company():
    branch = Branch(id=random.randint(10000, 999999))
    company = Company(
        id=random.randint(10000, 999999),
        name='Test Company',
        tariff='Enterprise',
        admin=Admin(email='example@mail.ru', password='password'),
        branches=[branch]),
    return company


@pytest.fixture(scope="session", autouse=True)
def prepare_env(request):
    _, profile, debug = get_profile()
    if profile == 'dev':
        pass

    # add functions to start before test session

    def clean():
        pass

    # add functions to start after all tests

    request.addfinalizer(clean)


def pytest_addoption(parser):
    parser.addoption("--profile", action="store", metavar="NAME",
                     help="test can be started only on the environment different from NAME.")


# register an additional marker
def pytest_configure(config):
    config.addinivalue_line("markers",
                            "ignore_on(name): mark tests to ignore on specified environment")


def pytest_runtest_setup(item):
    envmarker = item.get_closest_marker("ignore_on")
    if envmarker:
        for envname in envmarker.args:
            cfg, profile, _ = get_profile()
            if envname == profile:
                pytest.skip(f"test can not be started on {envname} environment")
