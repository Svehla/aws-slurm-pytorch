#!/usr/bin/env python
from src.config import config
from src.ssh_head_spawn_subprocess import ssh_head_spawn_subprocess
from src.rsync import rsync_to_head_node
from src.timer import timer
from app__run import install_project_libraries

# TODO: aws credentials are set because of s3 bucket service etc...
# I should set AWS IAM rules instead of /.aws/credentials
def setup_aws_credentials():
    ssh_head_spawn_subprocess('mkdir -p ~/.aws')
    rsync_to_head_node('./secrets/credentials_head_node_aws', '~/.aws/credentials')

# TODO: 
# I do support only 1 project per cluster? should I support multiple apps per pcluster?
# should the app decide which tool to use for setting up dependencies?
def install_head_node():
    cmds = [
        'sudo DEBIAN_FRONTEND=noninteractive apt-get update -y',
        # install venv globally for whole cluster
        'sudo DEBIAN_FRONTEND=noninteractive apt-get install -y python3-venv',
    ]

    for cmd in cmds:
        ssh_head_spawn_subprocess(cmd, activate_sources=False)
    

# took ~6min
@timer
def setup_cluster_lib_dependencies():
    install_head_node()
    # this should not be part of setup script but its handy to have it here
    install_project_libraries()
    setup_aws_credentials()
    print('--- script successfully ended ---')

def infra__cluster_setup():
    setup_cluster_lib_dependencies()

if __name__ == "__main__":
    infra__cluster_setup()