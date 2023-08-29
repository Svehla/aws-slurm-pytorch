#!/usr/bin/env python
from src.config import config
from src.head_node_ssh_communication import exec_sh_on_head_node
from exec__tensor_board_stop import stop_tensor_board
from exec__tensor_board_start import start_tensor_board
    
def reset_experiment(): 
    
    stop_tensor_board()
    tensor_board_experiment_path = '/shared/ai_app/tensor_board_logs'
    checkpoint_path = '/shared/ai_app/snapshots'

    exec_sh_on_head_node(f'rm -rf {tensor_board_experiment_path} 2>&1', pipe_output_to_print=True)

    exec_sh_on_head_node(f'rm -rf {checkpoint_path} 2>&1', pipe_output_to_print=True)

    start_tensor_board()



reset_experiment()