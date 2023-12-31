from src.cluster_state_utils import get_cluster_ip, get_subnet_id
from json5 import loads
from pathlib import Path
from src.json_validate import json_validate


# TODO: should be path to the config part of arg?
# Define the path to the file
file_path = Path('./user_cluster_config.jsonc')

# Read the file and load JSON data from it
user_config = loads(file_path.read_text())

json_validate(
    user_config,
    ["CLUSTER_NAME", "REGION", "PEM_PATH", "CURRENT_ACTIVE_APP_DIR", "AWS_KEY_PAIR_ID"],
    err_prefix="user_cluster_config.json is not valid,"
)

app_dir = user_config['CURRENT_ACTIVE_APP_DIR']

# this repo support 
# 1 instance of cluster
# N apps 
# Now we support only one app inside pcluster, but I could add support for more apps somehow
# TODO: have 2 configs, one for cluster, one for app?
class Config:
    # --- 1 cluster instance config ---
    CLUSTER_NAME = user_config['CLUSTER_NAME']
    REGION = user_config['REGION']
    PEM_PATH =  user_config['PEM_PATH']
    AWS_KEY_PAIR_ID =  user_config['AWS_KEY_PAIR_ID']

    # --- 1 app instance config --- 
    APP_DIR = app_dir
    LOCAL_APP = f"./apps/{app_dir}"
    LOCAL_APP_SRC = f"./apps/{app_dir}/app"
    HEAD_NODE_APP = f"/shared/{app_dir}"
    HEAD_NODE_APP_SRC = f"/shared/{app_dir}/app"
    HEAD_NODE_USER = "ubuntu"

config = Config()


# === fetch values if not defined, or refactor into terraform ===
# this is something like custom implementation of terraform state
class InfraState:
    @property
    def ip(self): 
        return get_cluster_ip(config.REGION, config.CLUSTER_NAME)

    @property
    def subnet_id(self):
        return get_subnet_id(config.REGION, config.CLUSTER_NAME)


infraState = InfraState()