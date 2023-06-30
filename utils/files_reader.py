import argparse
import csv
import fnmatch
import functools
import os

import yaml

from definitions import CONFIG_PATH, ROOT_DIR
from utils.decorator import func_once


class StringConcatinator(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = '!join'

    @classmethod
    def from_yaml(cls, loader, node):
        return functools.reduce(lambda a, b: a.value + b.value, node.value)


@func_once
def get_args():
    parser = argparse.ArgumentParser(argument_default=None)
    parser.add_argument('--profile', '-p', help='set active profile', dest='profile')
    parser.add_argument('--loadtest', '-lt', help='activate load test mode', dest='loadtest')
    parser.add_argument('--alluredir', '-ad', help='set allure directory', dest='alluredir', required=False)
    return parser.parse_known_args()[0]  # return only recognised values


"""it is possible to use local application.yaml file
 to keep configs or possible to send configuration properties via command line(has priority)"""


@func_once
def get_profile():
    with open(CONFIG_PATH, 'rt') as ymlfile:
        cfg = yaml.safe_load(ymlfile.read())
    active_profile = get_args().profile
    if active_profile is None:
        active_profile = cfg['profile']['active']
    if active_profile in cfg['profile']:
        profile = active_profile
    else:
        profile = 'dev'
    debug = cfg['profile']['debug']
    return cfg, profile, debug


@func_once
def app_config():
    cfg, profile, debug = get_profile()
    env_conf = {}
    env_conf.update(loadtest=cfg['profile']['loadtest'])
    env_conf.update(strict_validation=cfg['profile']['strict_validation'])
    env_conf.update(cfg['profile'][profile])
    env_conf.update(debug=debug)
    return env_conf


def recursive_glob(treeroot, pattern):
    results = []
    for base, dirs, files in os.walk(treeroot):
        good_files = fnmatch.filter(files, pattern)
        results.extend(os.path.join(base, f) for f in good_files)
    return results


def read_plugin_names():
    pattern = '*_fixture.py'
    fixture_paths = recursive_glob(ROOT_DIR, pattern)

    plugins = []
    for i, name in enumerate(fixture_paths):
        fixture_paths[i] = name.replace(name, name[:-3])
        fixture_paths[i] = fixture_paths[i].split(os.path.sep)
        plugins.append(fixture_paths[i][-3] + "." + fixture_paths[i][-2] + "." + fixture_paths[i][-1])
    return plugins


@func_once
def get_creds_from_file(path):
    my_list = []
    with open(path, mode='r') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            my_list.append(tuple(row))

    return my_list
