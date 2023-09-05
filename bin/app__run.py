#!/usr/bin/env python
from src.config import config
from src.ssh_head_spawn_subprocess import ssh_head_spawn_subprocess
from src.rsync import rsync_to_head_node
from src.timer import timer
from src.watch_sbatch_logs import watch_job_logs
import time

def upload_ml_model_into_head_node():
    ssh_head_spawn_subprocess(f"mkdir -p {config.HEAD_NODE_APP_SRC}", show_out=False)
    rsync_to_head_node(source_dir=config.LOCAL_APP_SRC, TARGET_DIR=config.HEAD_NODE_APP)

def install_project_libraries():
    upload_ml_model_into_head_node()
    ssh_head_spawn_subprocess(f"cd {config.HEAD_NODE_APP_SRC}; ./prepare_app_env.py")

# this is good but slow for development so I should hide it behind some cli param i guess
# SHOULD_prepare_app_env = True
SHOULD_prepare_app_env = False

@timer
def app__run():
    start_time = time.time()
    upload_ml_model_into_head_node()

    if SHOULD_prepare_app_env:
        install_project_libraries()

    out = ssh_head_spawn_subprocess(f"cd {config.HEAD_NODE_APP_SRC}; ./sbatch_exec.py")
    last_line_of_output = out.splitlines()[-1]
    batch_id = int(last_line_of_output.split()[-1])

    watch_job_logs(batch_id, start_time=start_time)

# boilerplate setup of ssh+rsync+slurm overhead took ~10sec
if __name__ == '__main__':
    app__run()

    # TODO: how to run `scancel {BATCH_ID}`? => should i automate it somehow?
    # 1. cmd+c => interruption signal 
    # 2. another .py script to exec it
