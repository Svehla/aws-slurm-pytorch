#!/usr/bin/env python

from src.ssh_head_spawn_subprocess import ssh_head_spawn_subprocess

def stop_tensor_board():
    ssh_head_spawn_subprocess('kill -9 $(lsof -t -i:6006) 2>&1')
    ssh_head_spawn_subprocess('rm -rf /shared/ai_app/tensor_board_output.log',)


if __name__ == '__main__':
    stop_tensor_board()