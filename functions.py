import yaml
import os
import sys
import six

class Compose_File: 
    def __init__(self):
        self.content = {}
        self.output = '/docker-compose.yml'

    def get_content(self):
        return self.content

    def set_content(self, content):
        self.content = content
        return self.content

    def get_output(self):
        return self.output

    def set_output(self, path):
        self.output = path
        return self.output

#yaml parse function

def yaml_parser(yaml_path):
    fullPath = os.path.join(os.path.dirname(os.path.abspath(__file__)) + yaml_path)
    with open(fullPath) as stream:
            try:
                config_yaml = (yaml.load(stream))
            except yaml.YAMLError as exc:
                print(exc)
    return config_yaml

#file writing function

def file_writer(yaml_path, data):
    fullPath = os.path.join(os.path.dirname(os.path.abspath(__file__)) + yaml_path)
    file = open(fullPath, 'w')
    yaml.dump(data, file, default_flow_style=False)

#yaml generation happens below

def yaml_generator(path, compose):
    config_yaml = yaml_parser(path)
    compose_yaml = yaml_parser(compose)
    compose_yaml = modify_yaml(config_yaml, compose_yaml)
    return compose_yaml

# The function that manages organized editing of the compose yaml

def modify_yaml(config_dict, compose_dict):
    config_title = next(iter(config_dict))
    for key in config_dict[config_title]:
        example = recursive_printer(compose_dict, key)
        new_value = six.moves.input(config_dict[config_title][key]['description'] + "\n" + "Example: " + example + '\n')
        recursive_replacer(compose_dict, key, new_value)
    return compose_dict

# A function that will recursively seek out and replace a value in a deeply nested dict

# def recursive_replacer(obj, search_key, value):
#     for key in obj:
#         if key == search_key:
#             obj[key] = value
#             print(obj)
#             return obj
#         elif type(obj[key]) == dict:
#            recursive_replacer(obj[key], search_key, value)

def recursive_replacer(obj, search_key, value):
    for key, val in obj.items():
        if isinstance(val, dict):
            obj[key] = recursive_replacer(val, search_key, value)
        if key == search_key:
            obj[key] = value
            return obj
    return obj


# A function that will retrieve a value in a deeply nested dict and return it.

def recursive_printer(obj, search_key):
    found_value = None
    for key, val in obj.items():
        if key == search_key:
            found_value = val
            if isinstance(found_value, list):
                found_value = found_value[0]
            break
        elif isinstance(val, dict):
            found_value = recursive_printer(obj[key], search_key)
            if found_value != None:
                break
    return found_value





# new_compose = yaml_generator('/config_files/dashboard.yml', '/docker-compose.yml')

# file_writer("/new-compose.yml", new_compose)

# new_compose = yaml_generator('/config_files/email.yml', '/new-compose.yml')

# file_writer("/new-compose.yml", new_compose)


