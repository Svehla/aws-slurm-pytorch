#!/usr/bin/env python3

# TODO: create python modules to fix it somehow
import sys
sys.path.append('/shared/jupyter_server/app') # fix shared import

from src.shared import create_prefixed_print, spawn_subprocess, stream_command_output
import time
import os

# TODO: resolve jump host log output for downloading of LLM models somehow
# import wget
# run llama locally on ubuntu:
# https://replicate.com/blog/run-llama-locally
# TODO: should it be run from head node, or compute node?

print = create_prefixed_print('[llama.cpp->prepare_app_env]') 

spawn_subprocess('echo "hello out of sh script"')

spawn_subprocess('pwd')

spawn_subprocess(f'source ~/apps/venv-app/bin/activate && pip3 install notebook')
