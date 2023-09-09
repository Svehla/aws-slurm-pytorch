#!/usr/bin/env python3
from src.timer import format_seconds_duration
import json
from src.config import config, infraState
from src.spawn_subprocess import spawn_subprocess
from src.magic_shells import colorize_red, clear_last_lines
from app__ssh_connect import escape_bash_quotes
import time
from functools import lru_cache
from src.timer import timer
from src.ssh_spawn_subprocess import cmd_over_ssh
from src.monitor_progress import monitor_progress 
# import tempfile
# import subprocess

# ml_ami == Machine learning ami
my_instance_name = 'custom-ml_ami_image_preparation'
# TODO: will AMI work even for different instance type with similar settings???
instance_type = 'g4dn.xlarge'

# ===== SUPER IMPORTANT LINE =====
# THERE SHOULD BE PCLUSTER AMI!!!!
# try to rebuild whole script with ami based on parallelcluster... ???
# THIS NEEDS TO BE FROM PCLUSTER INSTANCE => then we do not need to call 'aws ec2 wait image-available'
# there are details about picked instance
# https://eu-central-1.console.aws.amazon.com/ec2/home?region=eu-central-1#ImageDetails:imageId=ami-03d19ba6e04d6a411
parent_ec2_image = 'ami-03d19ba6e04d6a411'

def create_empty_ami():
    # aws region is default based on ~/.aws/config 
    # creation took around ~3min
    out = spawn_subprocess(' '.join([
        'aws ec2 run-instances',
        f'--image-id {parent_ec2_image}',
        '--count 1',
        f'--instance-type {instance_type}',
        f'--key-name {config.AWS_KEY_PAIR_ID}',
        f'--subnet-id {infraState.subnet_id}',
        # 125Gb disk is too small... xd NVCC needs large disks to be install properly
        '--block-device-mappings \'[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":200}}]\'',
        f''' --tag-specifications 'ResourceType=instance,Tags=[{{Key=Name,Value="{my_instance_name}"}}]' '''
    ]), show_out=False)

    out = json.loads(out)

    instance_id = out["Instances"][0]["InstanceId"]

    return instance_id

@lru_cache(maxsize=None)
def get_ec2_ip():
    ec2_ips = spawn_subprocess(' '.join([
        'aws ec2 describe-instances',
        f'--filters "Name=tag:Name,Values={my_instance_name}" '
        '--query "Reservations[*].Instances[*].PublicIpAddress" --output text'
    ]), show_out=False).split('\n')

    if len(ec2_ips) == 0:
        raise ValueError('no ec2 instance found')
    if len(ec2_ips) > 1:
        raise ValueError('more ec2 instances are spawn with the same name were found, check aws console to have only 1 running active instance!')

    return ec2_ips[0]

def ssh_head_spawn_subprocess(cmd):
    ip = get_ec2_ip()
    cmd_over_ssh('ubuntu', ip, config.PEM_PATH, cmd)

@timer
def install_deps_into_new_ec2():
    ssh_head_spawn_subprocess("echo 'installing os dependencies'")
    ssh_head_spawn_subprocess('sudo DEBIAN_FRONTEND=noninteractive apt-get update -y')
    ssh_head_spawn_subprocess('sudo DEBIAN_FRONTEND=noninteractive apt-get install -y nvidia-cuda-toolkit') # cuda compiler ~4min
    ssh_head_spawn_subprocess('nvcc --version')
    ssh_head_spawn_subprocess('sudo DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip python3-venv')
    ssh_head_spawn_subprocess(f'mkdir -p ~/apps') 
    
    # TODO: change path name to something less cringe
    venv_path = '~/apps/venv-app'

    ssh_head_spawn_subprocess(f'python3 -m venv {venv_path}') 

    # general python libraries shared across all /apps/{app} for simpler development
    ssh_head_spawn_subprocess(' && '.join([
        f'python3 -m venv {venv_path}',
        f'source {venv_path}/bin/activate',

        'pip3 install requests==2.31.0',
        'pip3 install torch==2.0.1',
        'pip3 install torchvision==0.15.2',
        'pip3 install boto3==1.28.33',
        # tensorboard is shared dependency between /bin cluster & /app
        'pip3 install tensorboard==2.14.0',
        'pip3 install numpy==1.24.4',
        'pip3 install notebook',
        # install
        # - jupyter notebook (and open it to internet+SSH tunnel to simulate google colab style)
    ]))

def get_ec_2_status(instance_id):
    out = spawn_subprocess(
        f'aws ec2 describe-instance-status --instance-ids {instance_id}', 
            show_out=False,
            show_cmd=False,
            show_time=False
        )
    out = json.loads(out)
    if len(out['InstanceStatuses']) == 0:
        return f'no ec2 instance with id: {instance_id} found'
    status = out['InstanceStatuses'][0]['SystemStatus']['Status']
    return status

def wait_till_ec2_is_ok(instance_id):
    print(f'start checking ec2: {instance_id} status')
    def is_loading_ended(prog_print):
        status = get_ec_2_status(instance_id)
        prog_print(status)
        return status == 'ok'

    monitor_progress(is_loading_ended)


def get_ec2_security_group_id(instance_id):
    out = spawn_subprocess(f"aws ec2 describe-instances --instance-ids {instance_id}", show_out=False)
    data = json.loads(out)
    instance = data['Reservations'][0]['Instances'][0]
    security_group = instance['SecurityGroups'][0]
    return security_group['GroupId']


# Build Custom ParallelCluster AMI from Custom Build Component
# what about to use `aws imagebuilder` instead of EC2 snapshot
@timer
def infra__create_custom_dl_ami():

    # instance_id = 'i-043469b2147b1378f'
    # === create a new EC2 instance ===
    instance_id = create_empty_ami()
    wait_till_ec2_is_ok(instance_id)

    # === Enable SSH connection into instance ===
    try:
        security_group_id = get_ec2_security_group_id(instance_id)
        spawn_subprocess(' '.join([
            'aws ec2 authorize-security-group-ingress',
            f'--group-id {security_group_id}',  # replace with your security group ID
            '--protocol tcp --port 22 --cidr 0.0.0.0/0',  # allows SSH traffic from any IP
        ]))
    except Exception as e:
        # skip error, if security-group-ingress is already set
        print(colorize_red(e))

    install_deps_into_new_ec2()

    out = spawn_subprocess(' '.join([
        'aws ec2 create-image',
        f'--instance-id {instance_id}',
        '--name "my_g4dn_ml_ami_instance_0"',
        '--description "custom image for cluster slurm machine learning with 1 GPU"'
    ])) # ~a few minutes
    out = json.loads(out)
    ami_image_id = out['ImageId']

    print('ami_image_id: ', ami_image_id)


    # ami_image_id = 'ami-0c078394f90de4df5'
    # print('image_id: ', ami_image_id)

    # TODO: add generic code for loading across whole bin 
    spawn_subprocess(f'aws ec2 wait image-available --image-ids {ami_image_id}')

    # ===== pcluster magic wrapper with magic errors ====
    # TODO: use pcluster instead of create-image
    # pcluster build-image --image-id myFirstCustomImage --image-configuration my-build-config.yaml
    # # store AMI into EBS:
    # Now I need to create AMI compatible with pcluster 
    # create_pcluster_ec2_image(ami_image_id)

    # TODO: terminate running EC2

    print('done!')

# boilerplate setup of ssh+rsync+slurm overhead took ~10sec
if __name__ == '__main__':
    infra__create_custom_dl_ami()



'''
# may be removed i guess, ec2 bash automating looks good, but not 100% sure about that
# mmmmm: this function is not needed anymore
# if I run ubuntu instance with bad AMI, it will throw random error in the cloudFormation stack
# if i go from pcluster ubuntu, everything works even without pcluster build-image
def create_pcluster_ec2_image(custom_ami_image):

    custom_pcluster_image_id = 'my-first-custom-image-0' # ???

    # Thanks to this I am gonna have pre-installed slurm and other stuffs needed to be run in the pcluster...
    with tempfile.NamedTemporaryFile('w', dir='./temp', suffix='_compiled_pcluster_config.yaml', delete=True) as temp_file:
        # shit yaml template...
        ec2_pcluster_image_config = f"""
Region: eu-central-1
Image:
    Name: My First Custom AMI for PCluster 3.0.0
Build:
    ParentImage: {custom_ami_image}
    InstanceType: {instance_type}
"""
        print(ec2_pcluster_image_config)
        temp_file.write(ec2_pcluster_image_config)
        temp_file.flush()

        cmd = ' '.join([
            'pcluster build-image',
            f'--image-id {custom_pcluster_image_id}',
            f'--image-configuration {temp_file.name}'
        ])
        spawn_subprocess(cmd)


    # watching logs
    # TODO: create some abstraction over While true status checking.... xd
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        # The whole process might take around 60 minutes or so, at the end of which all the resources used for the build will be deleted.
        out = spawn_subprocess(
            f'pcluster describe-image --image-id {custom_pcluster_image_id}',
            show_out=False,
            show_cmd=False
        )
        out = json.loads(out)
        subprocess.run('clear')
        print(format_seconds_duration(elapsed_time), out["imageBuildStatus"], out["cloudformationStackStatus"])
        time.sleep(3)
'''
