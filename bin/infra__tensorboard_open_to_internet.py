#!/usr/bin/env python3
# TODO: should I open tensorboard into internet or just do SSH tunnel into localhost
from src.config import infraState
from src.spawn_subprocess import spawn_subprocess
import requests


def check_url_availability(url):
    try:
        response = requests.get(url, timeout=2)
        response.raise_for_status()
    except Exception as err:
        return False
    else:
        return True

# to check security groups in the UI go to:
# https://eu-central-1.console.aws.amazon.com/ec2/home?region=eu-central-1#Home
def infra__tensorboard_open_to_internet():
    is_available = check_url_availability(f"http://{infraState.ip}:6006")

    if is_available:
        return

    # TODO: prefer to use boto3 somehow
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

    spawn_subprocess(' '.join([
        'aws ec2 authorize-security-group-ingress',
        f'--group-id {ec2_head_node_security_group_name}',
        '--protocol tcp --port 6006 --cidr 0.0.0.0/0',
    ]))


if __name__ == "__main__":
    infra__tensorboard_open_to_internet()

