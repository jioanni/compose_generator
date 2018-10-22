import yaml
import os
import fileinput

#yaml parse function

def yaml_parser(yaml_path):
    fullPath = os.path.join(os.path.dirname(os.path.abspath(__file__)) + yaml_path)
    with open(fullPath) as stream:
            try:
                config_yaml = (yaml.load(stream))
            except yaml.YAMLError as exc:
                print(exc)
    return config_yaml

def file_writer(yaml_path, data):
    fullPath = os.path.join(os.path.dirname(os.path.abspath(__file__)) + yaml_path)
    file = open(fullPath, 'w')
    yaml.dump(data, file, default_flow_style=False)

def yaml_generator(section, path):
    new_yaml = yaml_parser(path)
    obj = {section : {}}
    for key in new_yaml[section]:
        value = input(("Enter the {} (Default: " + str(new_yaml[section][key]) + ")\n").format(key))
        if key == "document_volume":
            value += ":/data/db"
        if key == "relational_volume":
            value += ":/var/lib/postgresql/data"
        if key == "data":
            value += ":/data"
        if key in ["port", "MailSmtpPort"]:
            value = int(value)
        if key in ["ssl", "MailStartTLS"]:
            value = value.lower()
            if value == "true":
                value = True
            else:
                value = False
        obj[section][key] = value
    new_yaml = obj
    file_writer(path, new_yaml)
