#!/usr/bin/env python3
from src.config import infraState
from src.spawn_subprocess import spawn_subprocess
    
def app__tensor_board_browser(): 
    spawn_subprocess(' '.join([
        'open',
        f"http://{infraState.ip}:6006"
    ]))


if __name__ == '__main__':
    app__tensor_board_browser()