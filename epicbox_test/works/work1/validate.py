import json
from os import path
from exceptions import InvalidConfigException

def validate_work_config(path):
    with open("config.json") as json_file:
        config = json.load(json_file)
        if config['name'] is None:
            raise InvalidConfigException("Laboratory work name is not set :(")
        if not isinstance(config['name'], str):
            raise InvalidConfigException("Laboratory work name should be str type :(")
        if (config['type'] is None) or (config['type'] != 'program') and (config['type'] != 'function') and (config['type'] != 'multiple'):
            raise InvalidConfigException("Laboratory work type is not set :(\nmust be: 'program' or 'function' or 'multiple'\n")
        if (config['language'] is None) or (config['language'] != 'c') or (config['language'] != 'c++'):
            raise InvalidConfigException("Laboratory work programming language is not set :(\nmust be 'c' or 'c++'")
        if config['default_limits'] is None:
            raise InvalidConfigException("Laboratory work default limits are not set :(")
        if config['type'] == 'multiple' and (config['exercises'] is None or \
            (not isinstance(config['exercises'], List)) or \
            (len(config['exercises']) < 2)):
                raise InvalidConfigException("Exercises settings are not set :(\nmust be a list of dictionaries")
        if config['type'] == 'multiple':
            if config['files'] is not None:
                raise InvalidConfigException("Files field should not be present when work type is 'multiple'")
            if config['tests'] is not None:
                raise InvalidConfigException("Tests field should not be present when work type is 'multiple'")
            for exercise in exersises:
                names = set()
                if exercise['subname'] is None:
                    raise InvalidConfigException("Exercise name is not set :(")
                if not isinstance(exercise['subname'], str):
                    raise InvalidConfigException("Exercise name should be str type :(")
                if exercise['subname'] in names:
                    raise InvalidConfigException("Exercise name should be unique :(")
                names.add(exercise['subname'])
                if exercise['type'] is None:
                    raise InvalidConfigException("Exercise type should be set :(")
                if exercise['type'] != 'program' or exercise['type'] != 'function':
                    raise InvalidConfigException("Exercise type should be 'program' or 'function'")
                if exercise['files'] is None:
                    raise InvalidConfigException("Exercise files are not set :(")
                if not isinstance(exercise['files'], List):
                    raise InvalidConfigException("Exercise files should be List type :(")
                if len(exercise['files']) < 1:
                    raise InvalidConfigException("Exercise files list is empty :(")
                if exercise['tests'] is None:
                    raise InvalidConfigException("Exercise tests settings are not set :(")
                if exercise['tests']['inputs_path'] is None:
                    raise InvalidConfigException("Exercise tests inputspath is not set :(")
                if not isinstance(exercise['tests']['inputs_path'], str):
                    raise InvalidConfigException("Exercise tests inputs path should be str type :(") 
                if exercise['tests']['outputs_path'] is None:
                    raise InvalidConfigException("Excercise tests outputs path is not set :(")
                if exercise['tests']['reference_path'] is not None:
                    if exercise['tests']['correct_outputs_path']:
                        raise InvalidConfigException("Exercice correct output path should not be present when reference is")
        if config['type'] != 'multiple' and config['exercises'] is not None:
            raise InvalidConfigException("'exersises' must not be set when 'type' is not 'multiple' :(")
        if config['type'] == 'program':
            if config['path_to_linkfiles'] is not None:
                raise InvalidConfigException("Program check should not contain path_to_linkfiles")
        print("ITS ALL GOOD")

validate_work_config("config.json")
