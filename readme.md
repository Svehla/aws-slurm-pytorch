# AWS slurm pytorch setup

This project automates the creation of an AWS ParallelCluster with one active application, utilizing N nodes and M GPUs.

## cli requirements:
- python
- pip
- awscli
- aws-parallelcluster

## Steps to setup cluster

```sh
# 0. copy proper .aws/credentials into /secrets/credentials_head_node_aws
# 1. init VPC + key_pair
./infra__cluster_vpc_init.py
# 2. create a new pcluster into the created VPC 
./infra__cluster_create.py
# 3. spawn slurm sbatch /app with basic ML script
./exec__run.py
# 4.check progress via tensorboard
./infra__tensorboard_open_to_internet.py
./exec__tensor_board_start.py
# 5. connect to the cluster via ssh to debug scripts
./exec__ssh_connect.py
# 6. destroy cluster head node to not to spend money
./infra__cluster_delete.py
```

## AWS GPU cost analysis

```
----------------------------------------
AWS GPU options summary:
https://docs.aws.amazon.com/dlami/latest/devguide/gpu.html

### P2 = NVIDIA K80 GPU
https://aws.amazon.com/ec2/instance-types/p2/
p2.xlarge     - 1 GPU ($0.900)
p2.8xlarge    - 8 GPU ($7.200)

### P3 = NVIDIA Tesla V100-SXM2-16GB
https://aws.amazon.com/ec2/instance-types/p3/
p3.2xlarge - 1 GPU ($3.06/h)
p3.2xlarge - 4 GPU ($12.24/h)

### P4 = NVIDIA A100 => too expensive
https://aws.amazon.com/ec2/instance-types/p4/

### G4 = AMD + NVIDIA 
NVIDIA Tesla T4 => THE BEST
g4dn.xlarge   - 1 NVIDIA GPU ($0.526/h)
g4dn.12xlarge - 4 NVIDIA GPU ($3.912/h)

### G3 = NVIDIA Tesla M60 => cheapest
https://aws.amazon.com/ec2/instance-types/g3/
g3.8xlarge    - 2 NVIDIA GPU ($2.28/h)
```



## /bin to /apps/{APP_ID} communication protocol

each app has 2 files that works as an API to enable automating infrastructure with app implementation

1. `install_deps.py` install deps inside of previously set venv

2. `./sbatch_exec.py` this file will be run => rename tu exec_run ????

all needs to use venv right now

### Bottlenecks to TODO

i hardcoded venv inside /bin in
1. ssh interactive connection
2. ssh non-interactive connection 
3. cluster_setup venv installation

### 1 cluster 1 active app (out of N) dependant to venv
by switching user_cluster_config.json['CURRENT_ACTIVE_APP_DIR'] you may develop 
1 cluster -> N apps 