#!/usr/bin/env python

from src.config import config
from src.head_node_ssh_communication import exec_sh_on_head_node
from src.rsync import rsync_to_head_node
from src.timer import timer
from src.watch_sbatch_logs import watch_job_logs

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
    exec_sh_on_head_node(f"cd {config.HEAD_NODE_APP_SRC}; ./install_deps.py", pipe_output_to_print=True)

# this is good but slow for development so I should hide it behind some cli param i guess
# SHOULD_INSTALL_DEPS = True
SHOULD_INSTALL_DEPS = False

@timer
def main_exec_slurm_job():
    # TODO: should I setup source code path from the arg to have option to switch codebase + executors
    # or just keep it for one training and do not crate platform for pcluster usage
    upload_source_code_into_head_node()

    if SHOULD_INSTALL_DEPS:
        install_project_libraries()

    out = exec_sh_on_head_node(f"cd {config.HEAD_NODE_APP_SRC}; ./sbatch_exec.py", pipe_output_to_print=True)
    last_line_of_output = out.splitlines()[-1]
    batch_id = int(last_line_of_output.split()[-1])

    watch_job_logs(batch_id)

if __name__ == '__main__':
    main_exec_slurm_job()

    # TODO: how to run `scancel {BATCH_ID}`? => should i automate it somehow?
    # 1. cmd+c => interruption signal 
    # 2. another .py script to exec it
