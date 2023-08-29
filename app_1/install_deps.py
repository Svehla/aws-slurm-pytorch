#!/usr/bin/env python3

from shared import create_prefixed_print, stream_command_output
print = create_prefixed_print('[head_inst]')

# ----- we need to be sure that venv is set correctly -----
# venv is set thanks to smart ssh executor which i programmed

# TODO: how to handle per app dependencies?
# this is event better if i would like to port local development into slurm cluster
# 1. conda, 
# 2. venv 
# 3. .tar of dockerImage (I think that this sucks, VirtualPCs 4ever)

# took ~4min
def install_deps():
    stream_command_output(f'pip3 install -r ./requirements.txt', print=print)


install_deps()
