
# AWS slurm pytorch JUMP HOST infrastructure tooling

This project automates the creation of an AWS ParallelCluster with one active application, utilizing N nodes and M GPUs.

## cli requirements:
- python
- pip
- awscli
- aws-parallelcluster

## Installations

```sh

pip install -r ./bin/requirements.txt
activate-global-python-argcomplete
echo "... ..." >> touch user_cluster_config.json 

# artificial software development
alias asd=~/Desktop/pytorch_parallel_training/bin/index.py

```



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

```sh
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

0. prepare shared DL preinstalled AMI

1. `./sbatch_prepare_app_env.py`

2. `./prepare_data.py` # TODO: not implemented yet

3. `./sbatch_exec.py` 

all needs to use venv right now

### Bottlenecks to TODO

I hardcoded venv inside /bin in a few places:
1. ssh interactive connection
2. ssh non-interactive connection 
3. cluster_setup venv installations

should the app decide which package manager it wants to use? 
venv cons:
- python specific (not needed for c++/c/js distributed apps)

### N clusters with N apps

`data/clusters/{cluster_namespace}/temp`

`data/clusters/{cluster_namespace}/secrets`

hen put data into .gitignore and change which cluster is active by changing user_cluster_config.json?

which just setup which instance is available for interaction right now?

