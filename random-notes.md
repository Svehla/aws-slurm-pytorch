
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
    - what about pcluster template?
    => it's look to complex to do another level of abstraction here
    - extract /app/shared + other reusable files for multi app spawning & developing

## Future
- create test web page that will spawn new node?


