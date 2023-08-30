#!/usr/bin/env python
from src.config import infraState
from src.spawn_subprocess import spawn_subprocess
    
def open_browser_with_tensor_board(): 
    spawn_subprocess(' '.join([
        'open',
        f"http://{infraState.ip}:6006"
    ]))


if __name__ == '__main__':
    open_browser_with_tensor_board()