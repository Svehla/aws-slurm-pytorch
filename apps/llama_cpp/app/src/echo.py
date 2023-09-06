#!/usr/bin/env python3


import sys
sys.path.append('/shared/llama_cpp/app/src') # fix shared import
# sys.path.append('/shared/llama_cpp/app/ml_model/src/download_multinode_dataset')
import time

# time.sleep(60 * 60) # hack to attach into running instance 

from shared import spawn_subprocess, stream_command_output, create_prefixed_print
print = create_prefixed_print('')
# print = create_prefixed_print('[llama->compute_srun]')

print('echo from src => should run llama')

spawn_subprocess('pwd', print=print)

chat_prompt =  "### what does GPT mean? in context of NLP?"

model = \
    'model.bin' # only working model right now...
    # 'pytorch_model-00001-of-00003.bin'
    # 'llama-2-13b-chat.ggmlv3.q3_K_M.bin'

print("Running llama.cpp sever")


"""

# === SSH tunnel to compute node for llama server ===
# TODO: automate ssh tunnel into .sh script into asd tool
# enable port forwarding
sudo vim /etc/ssh/sshd_config
AllowTcpForwarding yes
sudo systemctl restart ssh

pcluster ssh --cluster-name pytorch-ddp-tutor -o StrictHostKeyChecking=no -i ./secrets/secret_key_pair.pem -L 8080:pytorch-queue-1-gpu-dy-my-small-gpu-node-1:8080 -N
# pcluster ssh --cluster-name pytorch-ddp-tutor -o StrictHostKeyChecking=no -i ./secrets/secret_key_pair.pem -L 8080:10.0.2.177:8080 -N

# === llama grammar ===
# grammar:
https://grammar.intrinsiclabs.ai/

root ::= Question
Question ::= "{"   ws   "\"extractedQuestion\":"   ws   string   ","   ws   "\"answer\":"   ws   string   "}"
Questionlist ::= "[]" | "["   ws   Question   (","   ws   Question)*   "]"
string ::= "\""   ([^"]*)   "\""
boolean ::= "true" | "false"
ws ::= [ \t\n]*
number ::= [0-9]+   "."?   [0-9]*
stringlist ::= "["   ws   "]" | "["   ws   string   (","   ws   string)*   ws   "]"
numberlist ::= "["   ws   "]" | "["   ws   string   (","   ws   number)*   ws   "]"


# === system usage monitor ===
# fast GPU usage response via ssh attach
while true; do clear; nvidia-smi; sleep 0.2; done

"""
# ===================== server =====================
# run llama server:
# never ending task!
stream_command_output(' '.join([
    # run make only for the first time???? not sure
    'cd .. && cd llama.cpp &&',
    # 'make -j &&',
    './server',
    # '--seed 1337',
    f'-m ../models/{model}',
    '--n-gpu-layers 43',
    '--host 0.0.0.0', # enable to do the ssh tunnel + accepting req from other servers inside cluster
    # '-n 255', # max token output length
    # '-m ../models/llama-2-13b-chat.ggmlv3.q2_K.bin',
    # '--color -c 500 -b 192',
    # '--temp 0.0',
    # '--repeat_penalty 1.1 -n -1',
    # '-p "### Instruction: Write me a Python program that takes in user input and greets the user with their name.\n### Response:"'
    # f'-p "{chat_prompt}"'
]), print_std_error=True, print=print)

print("THIS SHOULD NEVER BE SHOWN!!!!!")


# TODO: download proper weights:
# https://github.com/ggerganov/llama.cpp#using-openllama
# TODO: compiling needs to be done on compute node, because: " warning: not compiled with GPU offload support,"
# TODO: test multiple cuda device setup
stream_command_output(' '.join([
    # run make only for the first time???? not sure
    'cd .. && cd llama.cpp &&',
    # 'make -j &&',
    './main',
    '--seed 1337',
    f'-m ../models/{model}',
    '--n-gpu-layers 43',
    '-n 255', # max token output length
    # '-m ../models/llama-2-13b-chat.ggmlv3.q2_K.bin',
    # '--color -c 500 -b 192',
    '--temp 0.0',
    # '--repeat_penalty 1.1 -n -1',
    # '-p "### Instruction: Write me a Python program that takes in user input and greets the user with their name.\n### Response:"'
    f'-p "{chat_prompt}"'
]), print_std_error=True, print=print)

# LLama GPU CLI exec
"""
./main -m ../models/model.bin \
./server -m ../models/model.bin \
    -i \
    --n-gpu-layers 43 \
    -p "hello, how are you?" -n 400 -e
"""

# TODO: run ./server + add ssh tunnel 