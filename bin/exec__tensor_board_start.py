#!/usr/bin/env python
import subprocess
from src.config import config
from src.head_node_ssh_communication import exec_sh_on_head_node
import time
from src.timer import format_seconds_duration
from exec__tensor_board_browser import open_browser_with_tensor_board

# TODO: 
# 1. remove tensorboard dependency + add removing prev output via cursor
# 2. use cursor lib to better refreshing stdout
def watch_server_log_file(path: str):
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time
        time.sleep(3)
        logOut = []
        try:
            logOut.append("=== Be sure that you opened tensorboard into the internet ===")
            logOut.append("")
            logOut.append(f"Elapsed time: {format_seconds_duration(elapsed_time)}")

            out = ''
            try:
                out = exec_sh_on_head_node(f"cat {path}", show_ssh_communication=False)
            except Exception as e:
                logOut.append(f'file on path: {path} does not exist')

            logOut.append(out)

            # run for N secs
            if elapsed_time > 20:
                logOut.append('=== stop watching output changes ===')
                print("\n".join(logOut))
                break

        except Exception as e:
            logOut.append(f'e: {str(e)} ')
            print("\n".join(logOut))
            break

        subprocess.run('clear')
        print("\n".join(logOut))



def start_tensor_board():
    print("=== Be sure that you opened tensorboard into the internet ===")
    exec_sh_on_head_node('rm /shared/ai_app/tensor_board_output.log 2>&1')

    # TODO: is smart to store logs into file into head node?
    exec_sh_on_head_node('nohup tensorboard --logdir=/shared/ai_app/tensor_board_logs --bind_all > /shared/ai_app/tensor_board_output.log 2>&1 &',)

    time.sleep(1)
    open_browser_with_tensor_board()

    watch_server_log_file('/shared/ai_app/tensor_board_output.log')
    

if __name__ == '__main__':
    start_tensor_board()


