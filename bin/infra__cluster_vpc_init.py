#!/usr/bin/env python

# TODO: rewrite this script into terraform + add option to delete all resources
# all of this can be done via aws parallel cluster CLI but its opaque and badly automated so the Terraform is the way
from src.config import config, infraState
from src.spawn_subprocess import spawn_subprocess
import boto3 
from pathlib import Path
from src.cluster_state_utils import invalidate_subnet_id_cache
import subprocess


ec2 = boto3.client('ec2', region_name=config.REGION)

"""
this is a little bit automated version of this tutorial:
create VPC by this tutorial: https://github.com/aws/aws-parallelcluster/blob/develop/README.md

1. create a "Amazon EC2 Key Pair "
2. create VPC
"""
def create_key_pairs():
    # duplicated with config file
    # TODO: should name of file be in the config as well?
    key_pair_name = f"key_pair_{config.CLUSTER_NAME}"

    response = ec2.create_key_pair(KeyName=key_pair_name)
    key_material = response['KeyMaterial']

    with open(config.PEM_PATH, 'w') as file:
        file.write(key_material)

    spawn_subprocess(f'chmod 400 {config.PEM_PATH}')
    return key_pair_name

vpc_name = f'VPC_{config.CLUSTER_NAME}'

def create_vpc_with_user_interaction():
    # unfortunately i'am not able to recreate pcluster setup, so we're using pcluster configure
    # I'am creating vpc by my own to define a name Tag properly for future infraState aws searching
    # check if vpc with this name already exists and if yes, throw new error
    # TODO: check if i can create 
    vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
    vpc_id = vpc['Vpc']['VpcId']
    # is this enough? or i should keep the whole config on pcluster configure???
    ec2.create_tags(Resources=[vpc_id], Tags=[ { 'Key': 'Name', 'Value': vpc_name }])
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={'Value': True})
    """
    pcluster configure setup
    Allowed values for EC2 Key Pair Name:
    1. key_pair_pytorch-ddp-tutor
    EC2 Key Pair Name [key_pair_pytorch-ddp-tutor]: 
    Allowed values for Scheduler:
    1. slurm
    2. awsbatch
    Scheduler [slurm]: 1
    Allowed values for Operating System:
    1. alinux2
    2. centos7
    3. ubuntu1804
    4. ubuntu2004
    5. rhel8
    Operating System [alinux2]: 4
    Head node instance type [t2.micro]: 
    Number of queues [1]: 
    Name of queue 1 [queue1]: 
    Number of compute resources for queue1 [1]: 
    Compute instance type for compute resource 1 in queue1 [t2.micro]: 
    Maximum instance count [10]: 
    Automate VPC creation? (y/n) [n]: n
    Allowed values for VPC ID:
    #  id                     name                     number_of_subnets
    ---  ---------------------  ---------------------  -------------------
    1  vpc-936e6af8                                                    3
    2  vpc-09e5ab1ed829c410f  VPC_pytorch-ddp-tutor                    0
    VPC ID [vpc-936e6af8]: 2
    There are no qualified subnets. Starting automatic creation of subnets...
    Allowed values for Availability Zone:
    1. eu-central-1a
    2. eu-central-1b
    3. eu-central-1c
    Availability Zone [eu-central-1a]: 1
    Allowed values for Network Configuration:
    1. Head node in a public subnet and compute fleet in a private subnet
    2. Head node and compute fleet in the same public subnet
    Network Configuration [Head node in a public subnet and compute fleet in a private subnet]: 2
    DNS Hostnames of the VPC vpc-09e5ab1ed829c410f must be set to True
    Creating CloudFormation stack...
    Do not leave the terminal until the process has finished.
    Stack Name: parallelclusternetworking-pub-20230828155813 (id: arn:aws:cloudformation:eu-central-1:787214262457:stack/parallelclusternetworking-pub-20230828155813/d5cc21f0-45bb-11ee-8675-0a433a97f286)
    Status: Public - CREATE_IN_PROGRESS                                     
    """
    # you need to interact with CLI
    # TODO: uncomment
    subprocess.call([
        "pcluster", "configure", 
        '--region', config.REGION,
        '--config', './__temp_hack_to_delete_pcluster_config.yaml'
    ])

    spawn_subprocess(f'rm -f ./__temp_hack_to_delete_pcluster_config.yaml')

 

def init_aws_vpc_infrastructure():
    # 1.
    key_pair_name = create_key_pairs()
    print(f"Key pair : {key_pair_name} created")
    # 2.
    vpc_id = create_vpc_with_user_interaction() 
    print(f"VPC      :{vpc_id} created")



init_aws_vpc_infrastructure()