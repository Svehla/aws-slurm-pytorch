#!/usr/bin/env python
from src.config import config

from src.ssh_head_spawn_subprocess import ssh_head_spawn_subprocess

def stop_tensor_board():
    ssh_head_spawn_subprocess('kill -9 $(lsof -t -i:6006) 2>&1')
    ssh_head_spawn_subprocess(f'rm -rf /shared/{config.APP_DIR}/tensor_board_output.log',)

if __name__ == '__main__':
    stop_tensor_board()