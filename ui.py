import argparse
import sys
from functions import *

compose_parser = argparse.ArgumentParser(description= "APIF Docker-Compose Generator")
compose_parser.add_argument('source', action="store", type=str)
compose_parser.add_argument('-e', '--email', const="/config_files/email.yml", nargs="?", help="Configure the email settings for the docker-compose file.")
compose_parser.add_argument('-d', '--dashboard', const="/config_files/dashboard.yml", nargs="?", help="Configure the email settings for the docker-compose file.")
compose_parser.add_argument('-p', '--postgres', const="/config_files/postgres.yml", nargs="?", help="Configure the Postgres (relational db) mounting directory for the docker-compose file.")
compose_parser.add_argument('-m', '--mongo', const="/config_files/mongo.yml", nargs="?", help="Configure the Mongo (document db) mounting directory for the docker-compose file.")
compose_parser.add_argument('-o', '--output', help="Provide a path/filename for the edited compose YAML.")

args = compose_parser.parse_args()

if len(sys.argv) == 1:
    compose_parser.print_help(sys.stderr)
    sys.exit(1)


compose_dict = Compose_File()

compose_dict.set_content(yaml_parser(args.source))

arguments = vars(args)

for argument in arguments:
    if (arguments[argument] != None) & (argument != 'source'):
        config_dict = yaml_parser(arguments[argument])
        compose_dict.set_content(modify_yaml(config_dict, compose_dict.content))

print(compose_dict.get_content())
