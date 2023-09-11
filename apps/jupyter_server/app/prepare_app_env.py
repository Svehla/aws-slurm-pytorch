#!/home/ubuntu/apps/venv-app/bin/python3 

# TODO: create python modules to fix it somehow
import sys
sys.path.append('/shared/jupyter_server/app') # fix shared import

from src.shared import create_prefixed_print, spawn_subprocess

print = create_prefixed_print('[llama.cpp->prepare_app_env]') 

# not sure, if pip3 inherit venv from shebang
# I think its not installed in the venv!
# spawn_subprocess(f'pip3 install notebook')
spawn_subprocess(f'. ~/apps/venv-app/bin/activate && pip3 install notebook')
