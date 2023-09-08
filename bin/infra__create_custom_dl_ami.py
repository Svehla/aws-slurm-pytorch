#!/usr/bin/env python3

from src.config import config, infraState
from src.spawn_subprocess import spawn_subprocess
# from src.compute_node import get_active_compute_nodes
from app__ssh_connect import escape_bash_quotes
# from src.config import config
# from src.array import filter_empty_items
    
# this is shared code with VPC infra setup
def get_cluster_security_group():
    # Took security group from the 
    instance_by_ip_res = spawn_subprocess(' '.join([
        f"aws ec2 describe-instances",
        "--query 'Reservations[*].Instances[*].[InstanceId,PublicIpAddress]'",
        f"--output text | grep {infraState.ip}",
    ]))

    instance_id = instance_by_ip_res.split()[0]

    ec2_head_node_security_group_name = spawn_subprocess(' '.join([
        'aws ec2 describe-instances '
        f'--instance-ids "{instance_id}"',
        '--query "Reservations[*].Instances[*].SecurityGroups[*].GroupId" --output text'
    ])).strip()

    return ec2_head_node_security_group_name

my_instance_name = 'kubas-custom-dl-ami'

def create_empty_ami():
    print('infra__create_custom_dl_ami')
    # create a virtual machine with preinstalled libraries
    # nvcc
    # venv
    #   pytorch
    #   pip -r requirements.txt # general AI ML libs

    # image_id = 'ami-my-custom-ami-id'
    
    # Ubuntu 64-bit (x86) => ID found on AWS CLI => i picked it
    image_id = 'ami-04e601abe3e1a910f'
    instance_type = 'g4dn.xlarge'

    ec2_head_node_security_group_name = get_cluster_security_group()
    print('ec2_head_node_security_group_name')
    print(ec2_head_node_security_group_name)

    # spawn_subprocess(' '.join([
    #     'aws ec2 describe-images',
    #     '--owners 099720109477',
    #     '--filters 'Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*' 'Name=state,Values=available' --query 'sort_by(Images, &CreationDate)[-1].[ImageId]' --output text --region eu-west-1
    # ]))
    # return

    out = spawn_subprocess(' '.join([
        'aws ec2 run-instances',
        f'--image-id {image_id}',
        '--count 1',
        f'--instance-type {instance_type}',
        # TODO: add region
        f'--key-name {config.AWS_KEY_PAIR_ID}',
        # is region coded in security group/subnet?
        f'--security-group-ids {ec2_head_node_security_group_name}',
        f'--subnet-id {infraState.subnet_id}'
        # TODO: fix escapings somehow
        f''' --tag-specifications 'ResourceType=instance,Tags=[{{Key=Name,Value="{my_instance_name}"}}]' '''
    ]), show_out=False)
    print(out)
    # TODO: wait, till instance is created and then return ip of a new instance


def get_ec2_ip_by_name():

    ec2_ip = spawn_subprocess(' '.join([
        'aws ec2 describe-instances',
        f'--filters "Name=tag:Name,Values={my_instance_name}" '
        '--query "Reservations[*].Instances[*].PublicIpAddress" --output text'
    ]), show_out=False)

    # print(ec2_ip)
    return ec2_ip


def ssh_head_spawn_subprocess(cmd):
    ip = get_ec2_ip_by_name()
    spawn_subprocess(' '.join([
        'ssh', 
        # automatically add host into ~/.ssh/known_hosts
        '-o StrictHostKeyChecking=no',
        '-i', config.PEM_PATH,
        f'ubuntu@{ip}', 
        f''' 'bash -c "{escape_bash_quotes(cmd)}"' '''
    ]))



def install_deps_into_new_ec2():
    
    ssh_head_spawn_subprocess("sudo apt-get update")
    ssh_head_spawn_subprocess("sudo DEBIAN_FRONTEND=noninteractive apt-get install -y nvidia-cuda-toolkit") # install cuda drivers
    spawn_subprocess("nvcc --version")

def infra__create_custom_dl_ami():
    # wait till instance is ready

    # create_empty_ami()
    install_deps_into_new_ec2()

    """
    jak vytvořit vlastní AMI na UBUNTU pomocí CLI na AWS, kde bude předinstalovaný python virtual env + pytorch 

    run ec2  

    install deps via SSH


    ssh -i "MyKeyPair.pem" ubuntu@ec2-198-51-100-1.compute-1.amazonaws.com
    sudo apt-get update
    sudo apt-get install python3-venv
    python3 -m venv myenv
    source myenv/bin/activate
    pip install torch
    aws ec2 create-image --instance-id i-1234567890abcdef0 --name "My server" --description "An image of my server"
    """

# boilerplate setup of ssh+rsync+slurm overhead took ~10sec
if __name__ == '__main__':
    infra__create_custom_dl_ami()



