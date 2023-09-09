#!/usr/bin/env python3


import sys
sys.path.append('/shared/jupyter_server/app/src') # fix shared import
import time

from shared import spawn_subprocess, stream_command_output, create_prefixed_print
print = create_prefixed_print('')

print('echo from src => should run jupyter notebook')

spawn_subprocess('pwd', print=print)

# ===================== server =====================
# run llama server:
# never ending task!
# run server took around ~1.5min
    


# TODO: add before_connection_config.template.sh ?
# command source is not available in /bin/sh... mmm what to do with it?

stream_command_output(' '.join([
    # i cant see logs....

    # no outputs for this code
    # f"/bin/bash -c '"
    # 'source ~/apps/venv-app/bin/activate &&'
    # 'jupyter notebook --ip 0.0.0.0 --port 9999'
    # "'"
    '. ~/apps/venv-app/bin/activate && jupyter notebook --ip 0.0.0.0 --port 9999'
]), print=print)

print("THIS SHOULD NEVER BE SHOWN!!!!!")
print("THIS SHOULD NEVER BE SHOWN!!!!!")
print("THIS SHOULD NEVER BE SHOWN!!!!!")
print("THIS SHOULD NEVER BE SHOWN!!!!!")
print("THIS SHOULD NEVER BE SHOWN!!!!!")
print("THIS SHOULD NEVER BE SHOWN!!!!!")
print("THIS SHOULD NEVER BE SHOWN!!!!!")
