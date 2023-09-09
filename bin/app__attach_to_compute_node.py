#!/usr/bin/env python3
from src.compute_node import get_active_compute_nodes
from app__ssh_connect import app__ssh_connect, escape_bash_quotes
from src.config import config
from src.array import filter_empty_items
    
def app__attach_to_compute_node():
    active_nodes = get_active_compute_nodes()
    print('TODO: implement attach_to_compute_node')
    print(active_nodes)

    node_to_connect = active_nodes[0]
    print(node_to_connect)
    print("TODO: select node which you want to connect")

    if not node_to_connect:
        print("TODO: no node is selected!!!!")
        return

    make_slurm_commands_available = 'source /etc/profile'
    commands_to_run_before_user_start_interacting = escape_bash_quotes('; '.join(filter_empty_items([
        make_slurm_commands_available,
        'source ~/.bashrc',
        f'cd /shared/{config.APP_DIR}',
    ])))

    # TODO: should  use before_connection_config.template.sh?
    ssh_conn_cmd = ' '.join([
        "ssh", 
        '-o StrictHostKeyChecking=no',
        node_to_connect['node'],
        "-t",
        # it looks that it works (--rcfile is too complex i guess)
        f""" "{commands_to_run_before_user_start_interacting}; bash -i" """
        # f'bash --rcfile <(echo "{commands_to_run_before_user_start_interacting}")'
        # escape_bash_quotes("'source /etc/profile; source ~/.bashrc; cd /shared/llama_cpp; bash -i'")
        # chatGPT magic :pray: god bless open.ai
    ])

    print('------------')
    print(ssh_conn_cmd)
    print()
    app__ssh_connect(ssh_conn_cmd)

# boilerplate setup of ssh+rsync+slurm overhead took ~10sec
if __name__ == '__main__':
    app__attach_to_compute_node()



