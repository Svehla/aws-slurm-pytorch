#!/usr/bin/env python

from src.head_node_ssh_communication import exec_sh_on_head_node

def stop_tensor_board():
    exec_sh_on_head_node('kill -9 $(lsof -t -i:6006) 2>&1')
    exec_sh_on_head_node('rm -rf /shared/ai_app/tensor_board_output.log',)


if __name__ == '__main__':
    stop_tensor_board()