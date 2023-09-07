# Random notes

## `TS` vs `PY` vs `terraform` for infrastructure code

### Python props
- infra people are using python more than JS
- easy to setup and run
- jupyter notebook ecosystem
- i could extract cluster infra into docker image similar as miob did
- not switching language context between app code + infra code

### TS props
- type inference
- better parallel execution calls
- better deps checks
- better module file system
- better prettier + eslint tooling



## TODO:
- Pytorch profiler https://pytorch.org/tutorials/intermediate/tensorboard_profiler_tutorial.html 
- what about wrap cli into docker image?
- nvidia hw profiler via CLI + via AWS dashboard cloudwatch
- Local development
- Jupyter notebook support
- TODO: how to develop models IRL?
- prod deployments
- add s3 data
- implement different SOTAs in this repo
- implement large LLM with pytorch RPC
- create Trainer class for DDP/RPC/Local development
- Add spot instances
- change bin into cmd installable tool with one instance => my cluster with extracted config file
    - before a do single cmd I need to figure out how to extract venv out of /bin/infra
    - extract config.py out of module
    - do a module venv for request + other libs
    - what about pcluster template? => it's look to complex to do another level of abstraction here
    - extract /app_1/shared + other reusable files for multi app spawning & developing
- create executable CLI command out of bin

## Future
- create test web page that will spawn new node?

### TODO:
how to create file structure of app? => do unify wrapper and then each app should be custom similar to custom git repo 


=> random ideas:


```sh
# targets:
# create reusable code for all apps:
# > local development
# > production inferring
# > cluster (slurm) runner code
#   > multi GPU training

/apps
    /{APP_ID}
        /requirements.txt # shared across local dev + head node
        /model # shared for local + slurm_node
            /model.py
            /dataset_preparation.py
            /trainer.py # generic trainer with tensorboard atd..
        /local_development
            /index.ipynb
            /localhost_trainer.py # ?
            /prepare_app_env.py
        /slurm_node_infra # multi GPU
            /sbatch_exec.py
            /srun_exec.py
            /multi_gpu_trainer.py
            /prepare_app_env.py
            /multinode_dataset_preparation.py # ??? what?

        /prepare_instance.py # install venv/conda/docker
        /shared # shared for slurm infra, slurm trainer, local trainer
            /shared_code # libs/whatever
        
        # prepare infrastructure with tensorboard somehow

        # python imports sucks, what about to create

# TODO: what about open jupyter on GPU with slurm node?
```