#!/usr/bin/env python
from src.config import config
from src.ssh_head_spawn_subprocess import ssh_head_spawn_subprocess
from src.rsync import rsync_to_head_node
from src.timer import timer
from exec__run import upload_source_code_into_head_node
from exec__run import install_project_libraries

# TODO: aws credentials are set because of s3 bucket service etc...
# I should set AWS IAM rules instead of /.aws/credentials
def setup_aws_credentials():
    ssh_head_spawn_subprocess('mkdir -p ~/.aws')
    rsync_to_head_node('./secrets/credentials_head_node_aws', '~/.aws/credentials')

# TODO: 
# should i use conda, or venv? 
# I do support only 1 project per cluster? should I support multiple apps per pcluster?
# should the app decide which tool to use for setting up dependencies?
def install_head_node_venv():
    # if yes, do i switch venv per project as well? => i guess that yes
    # if yes, venv setup should be handled by apps, not by cluster setup
    # HeadNode tensorboard is also installed into my-venv => TODO: use docker instead?
    cmds = [
        'sudo DEBIAN_FRONTEND=noninteractive apt-get update -y',
        'sudo DEBIAN_FRONTEND=noninteractive apt-get install -y python3-venv',
        'python3 -m venv /shared/ai_app/my-venv/',
        'echo "source /shared/ai_app/my-venv/bin/activate" >> ~/.bashrc',
    ]

    for cmd in cmds:
        ssh_head_spawn_subprocess(cmd, activate_sources=False)
    

# took ~6min
@timer
def setup_cluster_lib_dependencies():
    install_head_node_venv()
    # this should not be part of setup script but its handy to have it here
    install_project_libraries()
    setup_aws_credentials()
    print('--- script successfully ended ---')

if __name__ == "__main__":
    setup_cluster_lib_dependencies()