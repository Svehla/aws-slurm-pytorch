#!/usr/bin/env python3
from src.config import config

from src.ssh_head_spawn_subprocess import ssh_head_spawn_subprocess

def app__tensor_board_stop():
    ssh_head_spawn_subprocess('kill -9 $(lsof -t -i:6006) 2>&1')
    ssh_head_spawn_subprocess(f'rm -rf /shared/{config.APP_DIR}/tensor_board_output.log',)

if __name__ == '__main__':
    app__tensor_board_stop()