#!/home/ubuntu/apps/venv-app/bin/python3 
import sys
sys.path.append('/shared/jupyter_server/app/src') # fix shared import
from shared import stream_command_output, create_prefixed_print, debug_identify_instance
print = create_prefixed_print('')

print('=== running jupyter notebook server ===')

# testing venv import
import torch
print(torch.randn((1, 1)))


stream_command_output(' '.join([
    # venv struggles:
    # 1. shebang does not inherit to new spawn subprocesses
    # 2. source activate venv in sh is done via `.`
    '. ~/apps/venv-app/bin/activate && ',
    'jupyter notebook',
    '--ip 0.0.0.0',
    '--port 9999',

    # PAY ATTENTION, local development VSCODE BUG
    # if i want to connect from VSCode into the server, token needs to be set
    # it's probably some bug of VSCode plugin
    '--NotebookApp.token="1"',

    '--NotebookApp.password=""',
    # extra for vscode settings
    "--NotebookApp.allow_origin='*'",
    "--NotebookApp.ip='0.0.0.0'",
]), print=print)

print("THIS SHOULD NEVER BE SHOWN!!!!!")
print("THIS SHOULD NEVER BE SHOWN!!!!!")
print("THIS SHOULD NEVER BE SHOWN!!!!!")
print("THIS SHOULD NEVER BE SHOWN!!!!!")
print("THIS SHOULD NEVER BE SHOWN!!!!!")
print("THIS SHOULD NEVER BE SHOWN!!!!!")
print("THIS SHOULD NEVER BE SHOWN!!!!!")
