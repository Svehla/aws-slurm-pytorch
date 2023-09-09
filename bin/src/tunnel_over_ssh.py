from src.compute_node import get_active_compute_nodes
from src.config import config
from src.ssh_spawn_subprocess import ssh_head_spawn_subprocess
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
        f'-L {port}:{host}:{port} -N'
    ]))
