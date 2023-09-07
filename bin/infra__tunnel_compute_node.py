#!/usr/bin/env python3
from src.compute_node import get_active_compute_nodes
from src.config import config
from src.ssh_head_spawn_subprocess import ssh_head_spawn_subprocess
from src.spawn_subprocess import spawn_subprocess
import pprint
from src.magic_shells import colorize_red

enable_ssh_tunnel_config = 'AllowTcpForwarding yes'

def enable_head_node_ssh_tunneling():
    out = ssh_head_spawn_subprocess('cat /etc/ssh/sshd_config', show_out=False)

    if enable_ssh_tunnel_config in out:
        print(f"'{enable_ssh_tunnel_config}' already in the file")
    else: 
        ssh_head_spawn_subprocess(f'echo "{enable_ssh_tunnel_config}" | sudo tee -a /etc/ssh/sshd_config', show_out=False)
        ssh_head_spawn_subprocess('sudo systemctl restart ssh')

    print("SSH tunnel is enabled")


LLAMA_SERVER_PORT = 8080

def infra__tunnel_ssh(): 
    enable_head_node_ssh_tunneling()

    active_nodes = get_active_compute_nodes()
    print('TODO: implement selecting of active nodes')
    pprint.pprint(active_nodes)

    if len(active_nodes) != 1:
        print(colorize_red('only 1 compute node needs to exist to make this script works'))
        return

    node_to_connect = active_nodes[0]

    spawn_subprocess(' '.join([
        f'pcluster ssh --cluster-name {config.CLUSTER_NAME}',
        '-o StrictHostKeyChecking=no',
        f'-i {config.PEM_PATH}',
        # tunneling
        f' -L {LLAMA_SERVER_PORT}:{node_to_connect["node"]}:{LLAMA_SERVER_PORT} -N'
    ]))

if __name__ == "__main__":
    infra__tunnel_ssh()
