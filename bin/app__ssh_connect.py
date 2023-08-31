#!/usr/bin/env python

import os
from src.config import config

def run_pcluster():
    # exec vector path => execvp
    argv = [
        "pcluster", "ssh", 
        '-o StrictHostKeyChecking=no', # it automatically add host into the ~/.ssh/known_hosts
        "--cluster-name", config.CLUSTER_NAME, 
        "-i", 
        config.PEM_PATH,
        "-t",
        # chatGPT magic :pray: god bless open.ai
        f'bash --rcfile <(echo "source ~/.bashrc; source /shared/{config.APP_DIR}/my-venv/bin/activate")'
    ]


    os.execvp("pcluster", argv)

run_pcluster()
