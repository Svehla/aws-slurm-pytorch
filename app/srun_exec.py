#!/usr/bin/env python3
# this script runs on the single instance of computeNode
import os
import subprocess
import socket
import argparse

# ----- we need to be sure that venv is set correctly -----

# fix broken sbatch file system -> sbatch-ing this script has problem with local imports
import sys
sys.path.append('/shared/app/source_code')
sys.path.append('/shared/app/source_code/src/download_multinode_dataset')

from shared import create_prefixed_print, stream_command_output
from src.download_multinode_dataset import download_dataset
print = create_prefixed_print('[compute_srun]')

# downloading and preparing global shared node data before multinode training will start 
# this script si run when all resources are allocated but only one computeNode is running
# so its a little HW waste but we do not want to run training preparation on the head node
dataset_path = '/shared/app/train_datasets/mnist'
download_dataset(path=dataset_path, print=print)

# TODO: replace with stream_command_output
nodes = subprocess.check_output(f"scontrol show hostnames {os.getenv('SLURM_JOB_NODELIST')}", shell=True, text=True).split()
rdzv_node = nodes[0]
rdzv_node_ip = socket.gethostbyname(rdzv_node)
parser = argparse.ArgumentParser(description='simple distributed training job')
parser.add_argument('--experiment_name', type=str, help='')
parser.add_argument('--nodes_count', type=int, help='')
parser.add_argument('--gpus_per_node_count', type=int, help='')
args = parser.parse_args()

torchrun_cmd = ' '.join([
    "srun", "torchrun",
    "--nnodes", str(args.nodes_count),
    "--nproc_per_node", str(args.gpus_per_node_count),
    "--rdzv_id", str(os.getenv('RANDOM')),
    "--rdzv_backend", "c10d",
    "--rdzv_endpoint", f"{rdzv_node_ip}:29500",
    "./src/main_mnist_multinode.py",
    "--total_epochs", "5",
    "--save_every", "5",
    "--experiment_name", args.experiment_name,
    "--dataset_path", dataset_path,
    "--snapshots_dir", '../snapshots',
])

stream_command_output(torchrun_cmd)
