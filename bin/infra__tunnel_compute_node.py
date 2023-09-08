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

def open_ssh_tunnel_from_head_node(port, host='127.0.0.1'):
    spawn_subprocess(' '.join([
        f'pcluster ssh --cluster-name {config.CLUSTER_NAME}',
        '-o StrictHostKeyChecking=no',
        f'-i {config.PEM_PATH}',
        # tunneling into HEAD node
        f' -L {port}:{host}:{port} -N'
    ]))


LLAMA_SERVER_PORT = 8080

# TODO: what about open LLAMA into internet via public IP addr?
def infra__tunnel_ssh(): 
    enable_head_node_ssh_tunneling()

    active_nodes = get_active_compute_nodes()
    print('TODO: implement selecting of active nodes')
    pprint.pprint(active_nodes)

    if len(active_nodes) != 1:
        print(colorize_red('only 1 compute node needs to exist to make this script works'))
        return

    node_to_connect = active_nodes[0]

    # TODO: i do SSH tunnel into head node and then sending traffic from another node
    # TODO: there should be two ssh tunnels i guess
    open_ssh_tunnel_from_head_node(host=node_to_connect['node'], port=LLAMA_SERVER_PORT)

if __name__ == "__main__":
    infra__tunnel_ssh()

# pcluster ssh --cluster-name ddp-cluster -o StrictHostKeyChecking=no -i ./secrets/secret_key_pair.pem  -L 8080:pytorch-queue-1-gpu-dy-my-small-gpu-node-1:8080 -N
# pcluster ssh --cluster-name ddp-cluster -o StrictHostKeyChecking=no -i ./secrets/secret_key_pair.pem  -L 8080:pytorch-queue-1-gpu-dy-my-small-gpu-node-1:8080 -N