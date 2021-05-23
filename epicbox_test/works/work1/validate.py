import json
from os import path
from exceptions import InvalidConfigException
#ADD CORRECT_OUTPUTS_PATHS TO VALIDATION
#BETTER EXCEPTION MESSAGES
#DO EVERYTHING AFTER SLEEP
def validate_work_config(work_config_path: str):
    if not path.exists(work_config_path):
        raise InvalidConfigException("Config path [" + work_config_path +"  does not exist :(")
    with open(work_config_path) as json_file:
        config = json.load(json_file)
        if 'name' not in config:
            raise InvalidConfigException("Laboratory work name is not set :(")
        if not isinstance(config['name'], str):
            raise InvalidConfigException("Laboratory work name should be str type :(")
        if ('type' not in config) or (config['type'] != 'program') and (config['type'] != 'function') and (config['type'] != 'multiple'):
            raise InvalidConfigException("Laboratory work type is not set :(\nmust be: 'program' or 'function' or 'multiple'\n")
        if config['type'] == 'multiple' and (('exercises' not in config) or (not isinstance(config['exercises'], list)) or (len(config['exercises']) < 2)):
            raise InvalidConfigException("Laboratory work type 'multiple' should contain 'exercises' :(")
        if config['type'] != 'multiple' and 'exercises' in config:
            raise InvalidConfigException("'exersises' must not be set when 'type' is not 'multiple' :(")
        if config['type'] == 'program' and 'path_to_linkfiles' in config:
                raise InvalidConfigException("Program check type program should not contain path_to_linkfiles")
        if config['type'] == 'function' and 'path_to_linkfiles' not in config:
                raise InvalidConfigException("Program check type function should contain path_to_linkfiles")
        if ('language' not in config) or (config['language'] != 'c') and (config['language'] != 'c++'):
            raise InvalidConfigException("Laboratory work programming language is not set :(\nmust be 'c' or 'c++'")
        if 'default_limits' not in config:
            raise InvalidConfigException("Laboratory work default limits are not set :(")
        if config['default_limits'] != 'default':
            if 'cputime' not in config['default_limits']:
                raise InvalidConfigException("Laboratory work default limits must contain 'cputime'")
            if 'realtime' not in config['default_limits']:
                raise InvalidConfigException("Laboratory work default limits must contain 'realtime'")
            if 'memory' not in config['default_limits']:
                raise InvalidConfigException("Laboratory work default limits must contain 'memory'")
            if 'processes' not in config['default_limits']:
                raise InvalidConfigException("Laboratory work default limits must contain 'processes'")
        if config['type'] != 'multiple':
            if 'files' not in config:
                raise InvalidConfigException("'files' field should be present when work type is " + exercise['type'])
            if not isinstance(config['files'], list):
                raise InvalidConfigException("'files' field should be type 'list' :(")
            if len(config['files']) < 1:
                raise InvalidConfigException("Work 'files' field list is empty :(")
            if 'tests' not in config:
                raise InvalidConfigException("'tests' field should be present when work type is " + exercise['type']) 
            if 'inputs_path' not in config['tests']:
                raise InvalidConfigException("Work 'tests': 'inputs_path' is not set :(")
            if not isinstance(config['tests']['inputs_path'], str):
                raise InvalidConfigException("Work 'tests': 'inputs_path' should be str type :(")
            if not path.exists(config['tests']['inputs_path']) or not path.isdir(config['tests']['inputs_path']):
                raise InvalidConfigException("Work 'tests': 'inputs_path' no such directory")
            if 'outputs_path' not in config['tests']:
                raise InvalidConfigException("Work 'tests': 'outputs_path' is not set :(")
            if not isinstance(config['tests']['outputs_path'], str):
                raise InvalidConfigException("Work 'tests': 'outputs_path' should be str type :(")
            if not path.exists(config['tests']['outputs_path']) or not path.isdir(config['tests']['outputs_path']):
                raise InvalidConfigException("Work 'tests': 'outputs_path' no such directory")
            if 'reference_path' in config['tests'] and 'correct_outputs_path' in config['tests']:
                raise InvalidConfigException("Work 'tests': 'correct_outputs_path' should not be present when 'reference_path' is")
            if 'reference_path' in config['tests']: 
                if not isinstance(config['tests']['reference_path'], str):
                    raise InvalidConfigException("Work 'tests': 'reference_path' should be str type :(")
                if not path.exists(config['tests']['reference_path']) or not path.isdir(config['tests']['reference_path']):
                    raise InvalidConfigException("Work 'tests': 'reference_path' no such directory")
            else:
                if 'correct_outputs_path' not in exercise['tests']:
                    raise InvalidConfigException("Exercise 'correct_output_path' is not set :)\nYou can set 'reference_path' instead")
                if not isinstance(config['tests']['correct_outputs_path'], str):
                    raise InvalidConfigException("Work 'tests': 'correct_outputs_path' should be str type :(")
                if not path.exists(config['tests']['correct_outputs_path']) or not path.isdir(config['tests']['correct_outputs_path']):
                    raise InvalidConfigException("Work 'tests': 'reference_path' no such directory")
# add names of the exercise to every exception
        if config['type'] == 'multiple':
            if 'files' in config:
                raise InvalidConfigException("'files' field should not be present when work type is 'multiple'")
            if 'tests' in config:
                raise InvalidConfigException("'tests' field should not be present when work type is 'multiple'")
            for exercise in config['exercises']:
                names = set()
                if 'subname' not in exercise:
                    raise InvalidConfigException("Exercise 'subname' is not set :(")
                if not isinstance(exercise['subname'], str):
                    raise InvalidConfigException("Exercise 'subname' should be str type :(")
                if exercise['subname'] in names:
                    raise InvalidConfigException("Exercise 'subname' should be unique :(")
                names.add(exercise['subname'])
                if 'type' not in exercise:
                    raise InvalidConfigException("Exercise 'type' should be set :(")
                if exercise['type'] != 'program' and exercise['type'] != 'function':
                    raise InvalidConfigException("Exercise 'type' should be 'program' or 'function'")
                if exercise['type'] == 'program' and 'path_to_linkfiles' in exercise:
                    raise InvalidConfigException("Exercise type program check should not contain path_to_linkfiles")
                if exercise['type'] == 'function' and 'path_to_linkfiles' not in exercise:
                    raise InvalidConfigException("Exercise type function should contain path_to_linkfiles")
                if exercise['type'] == 'function' and (not path.exists(exercise['path_to_linkfiles'])):
                    raise InvalidConfigException("Exercise type function: 'path_to_linkfiles' does not exist")
                if 'files' not in exercise:
                    raise InvalidConfigException("Exercise " + exercise['subname'] +  " 'file's are not set :(")
                if not isinstance(exercise['files'], list):
                    raise InvalidConfigException("Exercise files should be List type :(")
                if len(exercise['files']) < 1:
                    raise InvalidConfigException("Exercise 'files' list is empty :(")
                if 'tests' not in exercise:
                    raise InvalidConfigException("Exercise tests settings are not set :(")
                if 'inputs_path' not in exercise['tests']:
                    raise InvalidConfigException("Exercise tests 'inputs_path' is not set :(")
                if not isinstance(exercise['tests']['inputs_path'], str):
                    raise InvalidConfigException("Exercise tests inputs path should be str type :(")
                if not path.exists(exerise['tests']['inputs_path']) or not path.isdir(exercise['tests']['inputs_path']):
                    raise InvalidConfigException("Exercise 'inputs_path' no such directory")
                if 'outputs_path' not in exercise['tests']:
                    raise InvalidConfigException("Excercise tests outputs path is not set :(")
                if not isinstance(exercise['tests']['outputs_path'], str):
                    raise InvalidConfigException("Exercise tests outputs path should be str type :(")
                if not path.exists(exerise['tests']['outputs_path']) or not path.isdir(exercise['tests']['outputs_path']):
                    raise InvalidConfigException("Exercise 'outputs_path' no such directory")
                if 'reference_path' in exercise['tests'] and 'correct_outputs_path' in exercise['tests']:
                        raise InvalidConfigException("Exercice 'correct_outputs_path' should not be present when 'reference_path' is")
                if 'reference_path' in exercise['tests']: 
                    if not isinstance(exercise['tests']['reference_path'], str):
                        raise InvalidConfigException("Exercise tests reference_path should be str type :(")
                    if not path.exists(exerise['tests']['reference_path']) or not path.isdir(exercise['tests']['reference_path']):
                        raise InvalidConfigException("Exercise 'reference_path' no such directory")
                else:
                    if 'correct_outputs_path' not in exercise['tests']:
                        raise InvalidConfigException("Exercise 'correct_output_path' is not set :)\nYou can set 'reference_path' instead")
        return True

if validate_work_config("config2.json"):
    print("CONFIG VALID")
else:
    print("CONFIG BAD :(")
