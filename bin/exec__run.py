#!/usr/bin/env python
from src.config import config
from src.head_node_ssh_communication import exec_sh_on_head_node
from src.rsync import rsync_to_head_node
from src.timer import timer
from src.watch_sbatch_logs import watch_job_logs
import time

# @timer
def upload_source_code_into_head_node():
    print(f"executing '{config.CODEBASE_SOURCE_DIR}' into parallel cluster")
    exec_sh_on_head_node(f"mkdir -p {config.HEAD_NODE_APP_SRC}")
    rsync_to_head_node(
        source_dir=config.CODEBASE_SOURCE_DIR,
        TARGET_DIR=config.HEAD_NODE_APP_SRC
    )

def install_project_libraries():
    upload_source_code_into_head_node()
    exec_sh_on_head_node(f"cd {config.HEAD_NODE_APP_SRC}; ./install_deps.py", show_out=True)

# this is good but slow for development so I should hide it behind some cli param i guess
# SHOULD_INSTALL_DEPS = True
SHOULD_INSTALL_DEPS = False

@timer
def main_exec_slurm_job():
    start_time = time.time()
    upload_source_code_into_head_node()

    if SHOULD_INSTALL_DEPS:
        install_project_libraries()

    out = exec_sh_on_head_node(f"cd {config.HEAD_NODE_APP_SRC}; ./sbatch_exec.py", show_out=True)
    last_line_of_output = out.splitlines()[-1]
    batch_id = int(last_line_of_output.split()[-1])

    watch_job_logs(batch_id, start_time=start_time)

# boilerplate setup of ssh+rsync+slurm overhead took ~10sec
if __name__ == '__main__':
    main_exec_slurm_job()

    # TODO: how to run `scancel {BATCH_ID}`? => should i automate it somehow?
    # 1. cmd+c => interruption signal 
    # 2. another .py script to exec it
