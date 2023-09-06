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
from infra__monitor_system_usage import infra__monitor_system_usage
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
from app__watch_sbatch import app__watch_sbatch
from app__attach_to_compute_node import app__attach_to_compute_node


infra_commands = [
    {
        "name": 'create_cluster__infra',
        "function": infra__cluster_create
    },
    {
        "name": 'delete_cluster__infra',
        "function": infra__cluster_delete
    },
    {
        "name": 'setup_cluster__infra',
        "function": infra__cluster_setup
    },
    {
        "name": 'status_cluster__infra',
        "function": infra__cluster_status
    },
    {
        "name": 'vpc_init_cluster__infra',
        "function": infra__cluster_vpc_init
    },
    {
        "name": 'vpc_remove_cluster__infra',
        "function": infra__cluster_vpc_remove
    },
    {
        "name": 'list_clusters__infra',
        "function": infra__clusters_list
    },
    {
        "name": 'monitor_system_usage__infra',
        "function": infra__monitor_system_usage
    },
    {
        "name": 'open_tensorboard_to_internet__infra',
        "function": infra__tensorboard_open_to_internet
    }
]

app_commands = [
    {
        "name": 'run__app',
        "function": app__run
    },
    {
        "name": 'ssh_connect__app',
        "function": app__ssh_connect
    },
    {
        "name": 'tensor_board_browser__app',
        "function": app__tensor_board_browser
    },
    {
        "name": 'start_tensor_board__app',
        "function": app__tensor_board_start
    },
    {
        "name": 'stop_tensor_board__app',
        "function": app__tensor_board_stop
    },
    {
        "name": 'watch_sbatch__app',
        "function": app__watch_sbatch
    },
    {
        "name": 'attach_to_compute_node__app',
        "function": app__attach_to_compute_node
    },
]

def find_command_by_name(name, commands):
    return next((command for command in commands if command['name'] == name), None)


infra_cmd_choices=[x['name'] for x in infra_commands]
app_cmd_choices=[x['name'] for x in app_commands]
all_cmd_choices = infra_cmd_choices + app_cmd_choices

def main():
    # TODO: read user_cluster_config.json or read data from cli args and setup config.py
    parser = argparse.ArgumentParser(description='', add_help=False)

    # namespaced version
    parser.add_argument(dest='task', choices=all_cmd_choices)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    module_function = find_command_by_name(args.task, infra_commands + app_commands)['function']
    module_function()

    """
    # namespaced CLI args version
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
    """
if __name__ == '__main__':
    main()
