#!/usr/bin/env python3

# ----- we need to be sure that venv is set correctly -----
# venv is set thanks to smart ssh executor which i programmed
# TODO: how to handle per app dependencies?
# this is event better if i would like to port local development into slurm cluster
# 1. conda, 
# 2. venv 
# 3. .tar of dockerImage (I think that this sucks, VirtualPCs 4ever)

import os
from ml_model.shared import create_prefixed_print, stream_command_output

from pathlib import Path
print = create_prefixed_print('[prepare_app_env]') # this should be printed by 

def check_folder_exists(folder_path):
    folder_path = Path(folder_path)
    return folder_path.is_dir()

# check if app-envs is exists, if yes, skip this step

if check_folder_exists('../venv') == False:
    stream_command_output(f'python3 -m venv ../venv-app/', print=print) 

os.system('')

stream_command_output(' && '.join([
    # there should not be `source {path}` cmd here
    '. ../venv-app/bin/activate',
    # needs to have activated venv (if not) to install pip3 deps
    'pip3 install -r ./requirements.txt'
]), print=print) # took ~4min
