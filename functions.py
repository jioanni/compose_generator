import yaml
import os
import sys

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
    new_yaml = yaml_parser(path)
    compose_yaml = yaml_parser(compose)
    compose_yaml = recursive_thing(new_yaml, compose_yaml)
    print(compose_yaml)


def recursive_thing(obj, compose_yaml, compose_section = None, compose_subsection = None, compose_key = None):
        for key in obj: 
            if "apifortress" in key:
                compose_section = key
                compose_subsection = next(iter(obj[key]))
            if type(obj[key]) == dict:
                compose_key = key
                recursive_thing(obj[key], compose_yaml, compose_section, compose_subsection, compose_key)
            elif obj[key] == obj['description']:
                if compose_key != compose_subsection:
                    user_input = input(obj['description'] + " (Datatype: " + obj['type'] + ") Default value: " + str(compose_yaml['services'][compose_section][compose_subsection][compose_key]) + "\n")
                    if user_input:
                        compose_yaml['services'][compose_section][compose_subsection][compose_key] = user_input
                else:
                    user_input = input(obj['description'] + " (Datatype: " + obj['type'] + ") Default value: " + str(compose_yaml['services'][compose_section][compose_subsection]) + "\n")
                    if user_input:
                        compose_yaml['services'][compose_section][compose_subsection] = user_input
        return compose_yaml



yaml_generator('/config_files/email.yml', '/docker-compose.yml')


