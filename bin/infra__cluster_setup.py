#!/usr/bin/env python
from src.config import config
from src.head_node_ssh_communication import exec_sh_on_head_node
from src.rsync import rsync_to_head_node
from src.timer import timer
from exec__sbatch import upload_source_code_into_head_node
from exec__sbatch import install_project_libraries

# TODO: aws credentials are set because of s3 bucket service etc...
# I should set AWS IAM rules instead of /.aws/credentials
def setup_aws_credentials():
    exec_sh_on_head_node('mkdir -p ~/.aws', pipe_output_to_print=True)
    rsync_to_head_node('./secrets/credentials_head_node_aws', '~/.aws/credentials')

# TODO: 
# should i use conda, or venv? 
# I do support only 1 project per cluster? should I support multiple apps per pcluster?
# should the app decide which tool to use for setting up dependencies?
def install_head_node_venv():
    # if yes, do i switch venv per project as well? => i guess that yes
    # if yes, venv setup should be handled by apps, not by cluster setup
    # HeadNode tensorboard is also installed into my-venv => TODO: use docker instead?
    exec_sh_on_head_node(
        [
            'sudo DEBIAN_FRONTEND=noninteractive apt-get update -y',
            'sudo DEBIAN_FRONTEND=noninteractive apt-get install -y python3-venv',
            'python3 -m venv /shared/ai_app/my-venv/',
            'echo "source /shared/ai_app/my-venv/bin/activate" >> ~/.bashrc',
        ],
        activate_sources=False,
        pipe_output_to_print=True,
    )
    

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