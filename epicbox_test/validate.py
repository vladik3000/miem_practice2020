import json
from sys import argv
import os

class InvalidConfigException(Exception):
    pass

def validate_limits(limits):
    if not isinstance(limits, dict):
        raise InvalidConfigException("limits field: should be dict")
    if 'cputime' not in limits:
        raise InvalidConfigException("Laboratory work limits must contain 'cputime'")
    if not isinstance(limits['cputime'], int):
        raise InvalidConfigException("limits cputime: " + str(limits['cputime']) + ": is not int")
    if 'realtime' not in limits:
        raise InvalidConfigException("Laboratory work default limits must contain 'realtime'")
    if not isinstance(limits['realtime'], int):
        raise InvalidConfigException("limits realtime: " + str(limits['realtime']) + ": is not int")
    if 'memory' not in limits:
        raise InvalidConfigException("Laboratory work default limits must contain 'memory'")
    if not isinstance(limits['memory'], int):
        raise InvalidConfigException("limits memory: " + str(limits['memory']) + ": is not int")
    if 'processes' not in limits:
        raise InvalidConfigException("Laboratory work default limits must contain 'processes'")
    if not isinstance(limits['processes'], int):
        raise InvalidConfigException("limits processes: " + str(limits['processes']) + ": is not int")

def validate_files(config):
    if 'files' not in config:
        raise InvalidConfigException("exercise: " + config['name'] + ": files field should be set")
    if not isinstance(config['files'], list):
        raise InvalidConfigException("exercise: " + config['name'] + ": files field should be list of strs")
    if len(config['files']) == 0:
        raise InvalidConfigException("exercise: " + config['name'] + ": files field list is empty")

def validate_essentials(config):
    if 'name' not in config:
        raise InvalidConfigException("Laboratory work name is not set :(")
    if not isinstance(config['name'], str):
        raise InvalidConfigException("Laboratory work name should be str type :(")
    if ('type' not in config) or (config['type'] != 'program') and (config['type'] != 'function') and (config['type'] != 'multiple'):
        raise InvalidConfigException("Laboratory work type is not set :(\nmust be: 'program' or 'function' or 'multiple'\n")
    if ('language' not in config) or (config['language'] != 'c') and (config['language'] != 'c++'):
        raise InvalidConfigException("Laboratory work programming language is not set :(\nmust be 'c' or 'c++'")
    if 'stop_if_fails' not in config:
        raise InvalidConfigException("stop_if_fails field not set :(\n should be true or false")
    if not isinstance(config['stop_if_fails'], bool):
        raise InvalidConfigException("config stop_if_fails field should be bool")
    if 'memcheck' not in config:
        raise InvalidConfigException("memcheck field not set :(\n should be true or false")
    if not isinstance(config['memcheck'], bool):
        raise InvalidConfigException("config memcheck field should be bool")
    if 'default_limits' not in config:
        raise InvalidConfigException("Laboratory work default limits are not set :(")
    validate_limits(config['default_limits'])

def validate_tests(tests):
    if 'outputs_path' not in tests:
        raise InvalidConfigException("config must contain outputs_path :(")
    if not os.path.isdir(tests['outputs_path']):
        raise InvalidConfigException("outputs_path: " + str(tests['outputs_path']) + ": no such directory")
    if 'reference' in tests and not os.path.isdir(tests['reference']):
        raise InvaludConfigException("reference path: " + str(tests['reference']) + ": no such directory")
    if 'reference' in tests and len(os.listdir(tests['reference'])) == 0:
        raise InvalidConfigException("reference directory: " + str(tests['reference']) + " is empty")
    if 'inputs_path' not in tests and 'reference' not in tests:
        if len(os.listdir(tests['outputs_path'])) != 1:
            raise InvalidConfigException("if inputs path is not set and reference is not set there should be only one output!")

def validate_function_type(config):
    if 'path_to_linkfiles' not in config:
        raise InvalidConfigException("task: " + config['name'] + ": path_to_linkfiles is not set when the type of task is function")
    if not isinstance(config['path_to_linkfiles'], str):
        raise InvalidConfigException("task: " + config['name'] + ": path_to_linkfiles is not str type")
    if not os.path.isdir(config['path_to_linkfiles']):
        raise InvalidConfigException("task: " + config['name'] + ": " + config['path_to_linkfiles'] + ": no suchdirectory")
    if len(os.listdir(config['path_to_linkfiles'])) == 0:
        raise InvalidConfigException("task: " + config['name'] + ": " + config['path_to_linkfiles'] + ": linkfiles dir is empty")

def validate_multiple(config):
    if ('exercises' not in config) or (not isinstance(config['exercises'], list)) or (len(config['exercises']) < 2):
        raise InvalidConfigException("Laboratory work type 'multiple' should contain 'exercises' :(")
    if 'files' in config:
        raise InvalidConfigException("'files' field should not be present when work type is 'multiple'")
    if 'tests' in config:
        raise InvalidConfigException("'tests' field should not be present when work type is 'multiple'")
    for exercise in config['exercises']:
        names = set()
        if 'name' not in exercise:
            raise InvalidConfigException("Exercise 'name' is not set :(")
        if not isinstance(exercise['name'], str):
            raise InvalidConfigException("Exercise 'name' should be str type :(")
        if exercise['name'] in names:
            raise InvalidConfigException("Exercise 'name' should be unique :(")
        names.add(exercise['name'])
        if 'limits' in exercise:
            validate_limits(exercise['limits'])
        if 'type' not in exercise:
            raise InvalidConfigError("exercise: " + exercise['name'] + " type is not set")
        if not isinstance(exercise['type'], str):
            raise InvalidConfigError("exercise: " + exercise['name'] + "type field is not str type")
        if exercise['type'] != 'function' and exercise['type'] != 'program':
            raise InvalidConfigError("exercise: " + exercise['name'] + "type : " + exercise['type'] + " is not 'function' or 'program'")
        if exercise['type'] == 'function':
            validate_function_type(exercise)
        if 'files' not in exercise:
            raise InvalidConfigException("exercise: " + exercise['name'] + ": files field should be set")
        validate_files(exercise)
        if 'tests' not in exercise:
            raise InvalidConfigException("exercise: " + exercise['name'] + ": tests field is not set")
        validate_tests(exercise)

def validate_work_config(work_dir: str):
    if not os.path.exists(work_dir):
        raise InvalidConfigException("lab directory with name: " + work_dir + " does not exist :(")
    work_config_path = os.path.join(work_dir, "config.json")
    if not os.path.isfile(work_config_path):
        raise InvalidConfigException("lab " + work_dir + " config file does not exist :(")
    with open(work_config_path) as json_file:
        config = json.load(json_file)
        validate_essentials(config)
        if config['type'] == 'multiple':
            validate_multiple(config)
        else:
            if config['type'] == 'function':
                validate_function_type(config)
            if 'exercises' in config:
                raise InvalidConfigException("'exersises' must not be set when 'type' is not 'multiple' :(")
            if 'files' not in config:
                raise InvalidConfigException("'files' field should be present when work type is " + str(exercise['type']))
            validate_files(config)
            if 'tests' not in config:
                raise InvalidConfigException("'tests' field should be present when work type is " + exercise['type']) 
            validate_tests(config['tests'])
# add names of the exercise to every exception
        return config
