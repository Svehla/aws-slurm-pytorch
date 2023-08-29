#!/usr/bin/env python
import subprocess
from src.config import infraState
    
def open_browser_with_tensor_board(): 
    subprocess.run([
        'open',
        f"http://{infraState.ip}:6006"
    ])


if __name__ == '__main__':
    open_browser_with_tensor_board()