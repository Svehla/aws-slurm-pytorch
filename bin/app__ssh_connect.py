#!/usr/bin/env python3


import os
from src.config import config
from src.ssh_head_spawn_subprocess import escape_bash_quotes
from pathlib import Path
from src.before_connection import sh_before_connection
from src.array import filter_empty_items

def read_file(file_path):
    file_path = Path(file_path)
    if file_path.exists():
        return file_path.read_text()
    else:
        return None


def app__ssh_connect():
    commands_to_run_before_user_start_interacting = escape_bash_quotes('; '.join(filter_empty_items([
        'source /etc/profile',
        'source ~/.bashrc',
        sh_before_connection,
        f'cd /shared/{config.APP_DIR}',
    ])))

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


if __name__ == '__main__':
    app__ssh_connect()