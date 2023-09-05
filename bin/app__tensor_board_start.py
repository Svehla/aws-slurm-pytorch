#!/usr/bin/env python
from src.config import config
from src.ssh_head_spawn_subprocess import ssh_head_spawn_subprocess
import time
from src.timer import format_seconds_duration
from app__tensor_board_browser import app__tensor_board_browser
from src.spawn_subprocess import spawn_subprocess

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
                out = ssh_head_spawn_subprocess(f"cat {path}", show_cmd=False, show_out=False)
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

        spawn_subprocess('clear')
        print("\n".join(logOut))



def app__tensor_board_start():
    print("=== Be sure that you opened tensorboard into the internet ===")
    ssh_head_spawn_subprocess(f'rm /shared/{config.APP_DIR}/tensor_board_output.log 2>&1', show_out=False)

    # TODO: is smart to store logs into file into head node?
    ssh_head_spawn_subprocess(
        f'nohup tensorboard --logdir=/shared/{config.APP_DIR}/tensor_board_logs --bind_all > /shared/{config.APP_DIR}/tensor_board_output.log 2>&1 &', 
        show_out=False
    )

    time.sleep(1)
    app__tensor_board_browser()

    watch_server_log_file(f'/shared/{config.APP_DIR}/tensor_board_output.log')
    

if __name__ == '__main__':
    app__tensor_board_start()


