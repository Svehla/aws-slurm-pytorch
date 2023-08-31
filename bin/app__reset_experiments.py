#!/usr/bin/env python
from src.config import config
from src.ssh_head_spawn_subprocess import ssh_head_spawn_subprocess
from app__tensor_board_stop import stop_tensor_board
from app__tensor_board_start import start_tensor_board
    
def reset_experiment(): 
    
    stop_tensor_board()
    tensor_board_experiment_path = f'/shared/{config.APP_DIR}/tensor_board_logs'
    checkpoint_path = f'/shared/{config.APP_DIR}/snapshots'

    ssh_head_spawn_subprocess(f'rm -rf {tensor_board_experiment_path} 2>&1')

    ssh_head_spawn_subprocess(f'rm -rf {checkpoint_path} 2>&1')

    start_tensor_board()

reset_experiment()