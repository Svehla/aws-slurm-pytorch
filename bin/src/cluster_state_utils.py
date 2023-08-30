import subprocess
from pathlib import Path
import boto3 
import json
from src.spawn_subprocess import spawn_subprocess

def fetch_aws_cluster_ip(region: str, cluster_name: str):
    # TODO: should I use boto3, or keep CLI as a main API?
    output = spawn_subprocess(' '.join([
        "pcluster", "describe-cluster",
        "--cluster-name", cluster_name,
        '--region', region
    ]))
    cluster_info = json.loads(output)
    public_ip = cluster_info['headNode']['publicIpAddress']
    return public_ip

def fetch_aws_first_vpc_subnet(region, vpc_name):
    ec2 = boto3.client('ec2', region_name=region)
    # find by name? it means that VPC has to be properly named...
    vpcs = ec2.describe_vpcs(Filters=[{ 'Name': 'tag:Name', 'Values': [vpc_name] }])

    if len(vpcs['Vpcs']) != 1:
        raise ValueError(f"there has to be only 1 vpc with name {vpc_name}")

    vpc_id = vpcs['Vpcs'][0]['VpcId']

    subnets = ec2.describe_subnets()

    def find_subnet_by_vpc_id(subnets, vpc_id):
        for subnet in subnets['Subnets']:
            if subnet['VpcId'] == vpc_id:
                return subnet

    subnet = find_subnet_by_vpc_id(subnets, vpc_id)
    return subnet['SubnetId']


# TODO: put it into ./state/....json
CACHE_FILE_PATH = './secrets/cluster_state_cache.json'

# --------------- cached cluster state ---------------
# TODO: refactor this to more abstract somehow => for example to rewrite it into terraform xd

def get_cluster_ip(region: str, clusterName: str):
    # TODO: add in memory cache????
    return _read_cluster_state_cache(
        'cluster_ip',
        lambda: fetch_aws_cluster_ip(region, clusterName)
    )

def invalidate_ip_cache():
    _write_cluster_state_cache('cluster_ip', None)

def get_subnet_id(region: str, cluster_name: str):
    return _read_cluster_state_cache(
        'subnet_id',
        lambda: fetch_aws_first_vpc_subnet(region, f'VPC_{cluster_name}')
    )

def invalidate_subnet_id_cache():
    _write_cluster_state_cache('subnet_id', None)

# ------------------------------------------------------------------
# --------------------- general cluster config ---------------------

# TODO: test if this fn is working properly
def _read_cluster_state_cache(key: str, fetch_data):
    file = Path(CACHE_FILE_PATH)

    if not file.exists():
        file.write_text(json.dumps({}))

    json_data = json.loads(file.read_text())

    value = json_data.get(key)

    if value == None:
        try:
            value = fetch_data()
            _write_cluster_state_cache(key, value)
        except Exception as e:
            print(e)
            pass

    return value

def _write_cluster_state_cache(key: str, value):
    file = Path(CACHE_FILE_PATH)

    if not file.exists():
        file.write_text(json.dumps({}))

    json_data = json.loads(file.read_text())

    json_data[key] = value

    file.write_text(json.dumps(json_data, indent=2))