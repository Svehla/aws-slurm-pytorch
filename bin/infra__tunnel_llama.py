#!/usr/bin/env python3
from src.compute_node import input_compute_node
from src.spawn_subprocess import spawn_subprocess
import pprint
from src.magic_shells import colorize_red

from src.tunnel_over_ssh import open_ssh_tunnel_from_head_node, enable_head_node_ssh_tunneling

LLAMA_SERVER_PORT = 9999 # 8080
JUPYTER_NOTEBOOK_PORT = 9999

# TODO: what about open LLAMA into internet via public IP addr?
def infra__tunnel_ssh(): 
    enable_head_node_ssh_tunneling()
    node_to_connect = input_compute_node()

    spawn_subprocess(f'open http://localhost:{LLAMA_SERVER_PORT}')
    # TODO: i do SSH tunnel into head node and then sending traffic from another node
    # TODO: there should be two ssh tunnels i guess
    open_ssh_tunnel_from_head_node(host=node_to_connect['node'], port=LLAMA_SERVER_PORT)

if __name__ == "__main__":
    infra__tunnel_ssh()
