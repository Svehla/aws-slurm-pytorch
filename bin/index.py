#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import argparse
import argcomplete, argparse
parser = argparse.ArgumentParser(description='simple distributed training job')

from infra__cluster_create import infra__cluster_create
from infra__cluster_delete import infra__cluster_delete
from infra__cluster_setup import infra__cluster_setup
from infra__cluster_status import infra__cluster_status
from infra__cluster_vpc_init import infra__cluster_vpc_init
from infra__cluster_vpc_remove import infra__cluster_vpc_remove
from infra__clusters_list import infra__clusters_list
from infra__system_monitor_usage import infra__system_monitor_usage
from infra__tensorboard_open_to_internet import infra__tensorboard_open_to_internet

# ---
#!/usr/bin/env python3
# above line is needed to be able to run the script as ./my-python.py

import argparse
import argcomplete

from app__run import app__run
from app__ssh_connect import app__ssh_connect
from app__tensor_board_browser import app__tensor_board_browser
from app__tensor_board_start import app__tensor_board_start
from app__tensor_board_stop import app__tensor_board_stop


infra_commands = [
    {
        "name": 'create_cluster',
        "function": infra__cluster_create
    },
    {
        "name": 'delete_cluster',
        "function": infra__cluster_delete
    },
    {
        "name": 'setup_cluster',
        "function": infra__cluster_setup
    },
    {
        "name": 'status_cluster',
        "function": infra__cluster_status
    },
    {
        "name": 'vpc_init_cluster',
        "function": infra__cluster_vpc_init
    },
    {
        "name": 'vpc_remove_cluster',
        "function": infra__cluster_vpc_remove
    },
    {
        "name": 'list_clusters',
        "function": infra__clusters_list
    },
    {
        "name": 'system_monitor_usage',
        "function": infra__system_monitor_usage
    },
    {
        "name": 'open_tensorboard_to_internet',
        "function": infra__tensorboard_open_to_internet
    }
]

app_commands = [
    {
        "name": 'run',
        "function": app__run
    },
    {
        "name": 'ssh_connect',
        "function": app__ssh_connect
    },
    {
        "name": 'tensor_board_browser',
        "function": app__tensor_board_browser
    },
    {
        "name": 'start_tensor_board',
        "function": app__tensor_board_start
    },
    {
        "name": 'stop_tensor_board',
        "function": app__tensor_board_stop
    },
]

def find_command_by_name(name, commands):
    return next((command for command in commands if command['name'] == name), None)

infra_cmd_choices=[x['name'] for x in infra_commands]
app_cmd_choices=[x['name'] for x in app_commands]

def main():
    # TODO: read user_cluster_config.json or read data from cli args and setup config.py
    parser = argparse.ArgumentParser(description='', add_help=False)
    subparsers = parser.add_subparsers(dest='namespace', help="")

    app_parser = subparsers.add_parser('app', add_help=False)
    app_parser.add_argument('task', choices=app_cmd_choices) 

    infra_parser = subparsers.add_parser('infra', add_help=False)
    infra_parser.add_argument('task', choices=infra_cmd_choices)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if args.namespace == 'infra':
        fn = find_command_by_name(args.task, infra_commands)
        fn['function']()
    elif args.namespace == 'app':
        fn = find_command_by_name(args.task, app_commands)
        fn['function']()

if __name__ == '__main__':
    main()
