#!/usr/bin/env python3
from src.shared import create_prefixed_print, spawn_subprocess
from ntb_conf import SHOULD_USE_GPU

print = create_prefixed_print('[jupyter->sbatch]')

cmd = ' '.join([
    "sbatch",

    f"--partition=pytorch-queue-{'1'if SHOULD_USE_GPU else '0'}-gpu",

    "--nodes=1",
    "--ntasks=1",
    "--gpus-per-task=1",
    "--cpus-per-task=4",
    "-o", "../slurm_output/%j-slurm.out",
    "./src/run_jupyter_notebook.py",
])

out = spawn_subprocess(cmd, show_out=False, print=print)

# this print needs to be there because output is parsed by ./bin/exec__run.py
print(out)
