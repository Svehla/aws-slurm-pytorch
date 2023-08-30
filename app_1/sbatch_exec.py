#!/usr/bin/env python3
import sys
import random
from shared import create_prefixed_print, spawn_subprocess, debug_identify_instance
print = create_prefixed_print('[head_sbatch]')

# ----- we need to be sure that venv is set correctly -----

# --- setting up global config for training instance ---
# if you want to change the config of your NN experiment this is definitely the place for you
# 4 nodes has problem because AWS do not want to allocate the resources for me! slurm error squeue note: 
# (Nodes required for job are DOWN, DRAINED or reserved for jobs in higher priority partitions)
NODES_COUNT = 1
GPUS_PER_NODE_COUNT = 1
EXPERIMENT_NAME = f"{random.randint(0, 10000)}-test_of_n{NODES_COUNT}-g{GPUS_PER_NODE_COUNT}"

gpu_partition_map = {
    1: "pytorch-queue-1-gpu",
    2: "pytorch-queue-2-gpu",
    4: "pytorch-queue-4-gpu"
}

try:
    partition = gpu_partition_map[GPUS_PER_NODE_COUNT]
except KeyError:
    print("Invalid GPUS_PER_NODE_COUNT. It must be 1, 2, or 4.")
    sys.exit(1)

# print("-------------------------")
# print(f"EXPERIMENT_NAME: {EXPERIMENT_NAME}")
# print(f"NODES_COUNT: {NODES_COUNT}")
# print(f"GPUS_PER_NODE_COUNT: {GPUS_PER_NODE_COUNT}")
# print("-------------------------")

"""
1. sbatch allocates requested nodes for your job and initiates your script on one of
these nodes, while srun within the script distributes tasks among these nodes.

2. For running a job using torchrun on multiple nodes with multiple GPUs, set
nnodes and --ntasks equal to the number of nodes in your SLURM script.

3. Within the torchrun command, set --nnodes and --nproc_per_node to specify
the distribution of processes across nodes and GPUs.
"""
cmd = ' '.join([
    "sbatch",
    "--partition=" + partition,
    "--nodes=" + str(NODES_COUNT),
    "--ntasks=" + str(NODES_COUNT),
    "--gpus-per-task=" + str(GPUS_PER_NODE_COUNT),
    "--cpus-per-task=4",
    "--job-name=app-multinode-" + EXPERIMENT_NAME,
    "-o", "../slurm_output/%j-slurm.out",
    "./srun_exec.py",
    f'--experiment_name={EXPERIMENT_NAME}',
    f'--nodes_count={NODES_COUNT}',
    f'--gpus_per_node_count={GPUS_PER_NODE_COUNT}',
])

out = spawn_subprocess(cmd, show_out=False, print=print)

# this print needs to be there because output is parsed by ./bin/exec__run.py
print(out)
