#!/usr/bin/env python3
from src.compute_node import get_active_compute_nodes
from src.config import config
from src.ssh_spawn_subprocess import ssh_head_spawn_subprocess
from src.spawn_subprocess import spawn_subprocess
import pprint
from src.magic_shells import colorize_red

from src.tunnel_over_ssh import open_ssh_tunnel_from_head_node, enable_head_node_ssh_tunneling

JUPYTER_NOTEBOOK_PORT = 9999

def infra__tunnel_ssh(): 
    enable_head_node_ssh_tunneling()

    print('TODO: implement selecting of active nodes')
    active_nodes = get_active_compute_nodes()
    pprint.pprint(active_nodes)
    if len(active_nodes) != 1:
        # TODO: add user picking of instance
        print(colorize_red('exactly 1 compute node needs to exist to make this script works'))
        return
    node_to_connect = active_nodes[0]


    spawn_subprocess(f'open http://localhost:{JUPYTER_NOTEBOOK_PORT}')
    # TODO: i do SSH tunnel into head node and then sending traffic from another node
    # TODO: there should be two ssh tunnels i guess
    open_ssh_tunnel_from_head_node(host=node_to_connect['node'], port=JUPYTER_NOTEBOOK_PORT)

if __name__ == "__main__":
    infra__tunnel_ssh()
