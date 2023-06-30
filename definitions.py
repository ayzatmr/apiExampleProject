import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'application.yaml')
LOGGER_CONF_PATH = os.path.join(ROOT_DIR, 'logger', 'log.yaml')
RESOURCES = os.path.join(ROOT_DIR, 'resources')
CUSTOMER_CREDENTIALS = os.path.join(RESOURCES, 'locust', 'customer_creds')
ADMIN_CREDENTIALS = os.path.join(RESOURCES, 'locust', 'admin_creds')
