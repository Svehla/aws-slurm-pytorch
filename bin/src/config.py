from src.cluster_state_utils import get_cluster_ip, get_subnet_id

# this repo support only one instance of pcluster
# Now we support only one app inside pcluster, but I could add support for more apps somehow
class Config:
    # --- cluster config ---
    CLUSTER_NAME = "pytorch-ddp-tutor"
    REGION = "eu-central-1"
    PEM_PATH = f"./secrets/ssh_key_pair.pem"


    # --- app config --- 
    # TODO:
    # there could be N apps in the future
    # to implement generic platform for multi node learning
    # TODO: venv could have same name as codebase source dir and could be change dynamically per app?
    # CURRENT_ACTIVE_APP=???
    HEAD_NODE_APP_SRC = "/shared/ai_app/source_code"
    HEAD_NODE_USER = "ubuntu"
    CODEBASE_SOURCE_DIR = "./app_1/"

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