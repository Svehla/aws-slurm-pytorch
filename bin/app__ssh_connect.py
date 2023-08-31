#!/usr/bin/env python

import os
from src.config import config
from src.ssh_head_spawn_subprocess import escape_bash_quotes

def run_pcluster():
    commands_to_run_before_user_start_interacting = escape_bash_quotes('; '.join([
        'source /etc/profile',
        'source ~/.bashrc',
        f'source /shared/{config.APP_DIR}/my-venv/bin/activate',
        f'cd /shared/{config.APP_DIR}',
    ]))

    # exec vector path => execvp
    argv = [
        "pcluster", "ssh", 
        '-o StrictHostKeyChecking=no', # it automatically add host into the ~/.ssh/known_hosts
        "--cluster-name", config.CLUSTER_NAME, 
        "-i", 
        config.PEM_PATH,
        "-t",
        # chatGPT magic :pray: god bless open.ai
        f'bash --rcfile <(echo "{commands_to_run_before_user_start_interacting}")'
    ]


    os.execvp("pcluster", argv)

run_pcluster()
