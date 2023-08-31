#!/usr/bin/env python
from src.cluster_status import show_cluster_status_progress
from src.config import config, infraState
from infra__cluster_setup import setup_cluster_lib_dependencies
from src.timer import timer
from src.spawn_subprocess import spawn_subprocess
from pathlib import Path
import tempfile

def compile_pcluster_config_template():
    pcluster_template = Path('pcluster_config_template.yaml').read_text()

    return pcluster_template \
        .replace(
            '{{SSH_HEAD_NODE_KEY_PAIR_NAME}}',
            # TODO: should i have shared key_pair across clusters? or generate shared one for all clusters
            f"key_pair_{config.CLUSTER_NAME}"
        ) \
        .replace('{{REGION}}', config.REGION) \
        .replace('{{SUBNET_ID}}', infraState.subnet_id)


# creating cluster took different time based on the HeadNode EC2 configuration
# ~ 8min - small instance like: t2.micro without /shared
# ~14min - larger as c5.large with FsxLustre shared file system
@timer
def spawn_cluster_creation():

    pcluster_config_yaml = compile_pcluster_config_template()

    with tempfile.NamedTemporaryFile('w', dir='./temp', suffix='_compiled_pcluster_config.yaml', delete=True) as temp_file:
        temp_file.write(pcluster_config_yaml)
        temp_file.flush()

        cmd = ' '.join([
            "pcluster", "create-cluster",
            "--cluster-configuration",
            temp_file.name,
            # temp_file.path,
            "--cluster-name", config.CLUSTER_NAME,
            "--region", config.REGION
        ])

        spawn_subprocess(cmd)

    show_cluster_status_progress()

# took ~18-21min
@timer
def create_set_cluster():
    try:
        spawn_cluster_creation()
        print("start installing py dependencies")
        print("________________________________")

        # progress ended, so now I'am able to get IP address of the HeadNode cluster
        setup_cluster_lib_dependencies()
    except Exception as e:
        print(f"An error occurred:")
        print(e)

create_set_cluster()