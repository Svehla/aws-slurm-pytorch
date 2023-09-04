#!/usr/bin/env python

import os
from src.config import config
from src.ssh_head_spawn_subprocess import escape_bash_quotes
from pathlib import Path
from src.before_connection import sh_before_connection


def read_file(file_path):
    file_path = Path(file_path)
    if file_path.exists():
        return file_path.read_text()
    else:
        return None

def run_pcluster():
    commands_to_run_before_user_start_interacting = escape_bash_quotes('; '.join([
        'source /etc/profile',
        'source ~/.bashrc',
        sh_before_connection,
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
