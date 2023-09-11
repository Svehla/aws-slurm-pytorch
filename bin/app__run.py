#!/usr/bin/env python3
from src.config import config
from src.ssh_spawn_subprocess import ssh_head_spawn_subprocess
from src.rsync import rsync_to_head_node
from src.timer import timer
from src.watch_sbatch_logs import watch_job_logs
import time
from src.magic_shells import colorize_red

def upload_ml_model_into_head_node():
    ssh_head_spawn_subprocess(f"mkdir -p {config.HEAD_NODE_APP_SRC}", show_out=False)
    rsync_to_head_node(source_dir=config.LOCAL_APP_SRC, TARGET_DIR=config.HEAD_NODE_APP)

def install_project_libraries():
    # TODO: spawn installation on compute node via sbatch and store packages on /shared fs
    upload_ml_model_into_head_node()

    start_time = time.time()
    # should i setup head node /shared fs via spawning slurm job via sbatch? 
    # TODO: move this installation into /app/{APP_ID}
    out = ssh_head_spawn_subprocess(' '.join([
        f"cd {config.HEAD_NODE_APP_SRC};",
        "./sbatch_prepare_app_env.py",
    ]))
    last_line_of_output = out.splitlines()[-1]
    batch_id = int(last_line_of_output.split()[-1])
    watch_job_logs(batch_id, start_time=start_time)
    # ssh_head_spawn_subprocess(f"cd {config.HEAD_NODE_APP_SRC}; ./prepare_app_env.py")

# this is good but slow for development so I should hide it behind some cli param i guess
SHOULD_prepare_app_env = False
# SHOULD_prepare_app_env = True

scancel_finished = False

@timer
def app__run():
    start_time = time.time()
    upload_ml_model_into_head_node()

    # TODO: read args and send it into compute node script
    # print('aaa')
    if SHOULD_prepare_app_env:
        install_project_libraries()
    # print('bbb')

    out = ssh_head_spawn_subprocess(f"cd {config.HEAD_NODE_APP_SRC}; ./sbatch_exec.py")
    last_line_of_output = out.splitlines()[-1]
    batch_id = int(last_line_of_output.split()[-1])

    # ---- if user click to CMD+C i want to scancel current slurm PID ----
    def signal_handler(sig, frame):
        global scancel_finished
        if scancel_finished:
            print(f'You pressed {colorize_red("Ctrl+C!")} again, killing the process, waited just for scancel. Be sure that everything is killed properly')
            os.kill(os.getpid(), signal.SIGTERM)
        else:
            print(f'You pressed {colorize_red("Ctrl+C!")}, wait till slurm job will be cancelled')
            ssh_head_spawn_subprocess(f"scancel {batch_id}")
            scancel_finished = True
            # is this code OK? not sure if i want to kill it... mmmm
            # os.kill(os.getpid(), signal.SIGTERM)

    signal.signal(signal.SIGINT, signal_handler)
    # ---- ---------------------------------------------------------- ----

    watch_job_logs(batch_id, start_time=start_time)


import os
import signal
import subprocess
import time


# boilerplate setup of ssh+rsync+slurm overhead took ~10sec
if __name__ == '__main__':
    app__run()

    # TODO: how to run `scancel {BATCH_ID}`? => should i automate it somehow?
    # 1. cmd+c => interruption signal 
    # 2. another .py script to exec it
