#!/usr/bin/env python3
from src.shared import create_prefixed_print, spawn_subprocess, debug_identify_instance
print = create_prefixed_print('[llama->head_sbatch]')

cmd = ' '.join([
    "sbatch",
    "--partition=pytorch-queue-1-gpu",
    "--nodes=1",
    "--ntasks=1",
    "--gpus-per-task=1",
    "--cpus-per-task=4",
    "-o", "../slurm_output/%j-slurm.out",
    "./prepare_app_env.py",
])

out = spawn_subprocess(cmd, show_out=False, print=print)

# this print needs to be there because output is parsed by ./bin/exec__run.py
print(out)

