#!/usr/bin/env python3

import os
from src.shared import create_prefixed_print, spawn_subprocess, stream_command_output
import time
# import wget

# run llama locally on ubuntu:
# https://replicate.com/blog/run-llama-locally
# TODO: should it be run from head node, or compute node?

print = create_prefixed_print('[llama.cpp->prepare_app_env]') 

repo_url = "https://github.com/ggerganov/llama.cpp"
local_path = "llama.cpp"

is_cloned = os.path.exists(f'../{local_path}')
print('ahoj')
print(is_cloned)
spawn_subprocess("pwd")

if not is_cloned:
    # Repo does not exist locally, clone it
    spawn_subprocess(f'cd .. && git clone {repo_url} {local_path}', print=print)
else:
    # Repo exists locally, update it
    spawn_subprocess(f'cd .. && git -C {local_path} pull', print=print)

# === downloading dataset should be in the different module, not prepare_app_env ===
# TODO: download LLama weights

# TODO: build via make LLAMA_CUBLAS=1?
# https://dev.to/timesurgelabs/how-to-run-llama-2-on-anything-3o5m

# downloading do not respond right now...
# it looks that wget/curl do not return new line, so the progress bar is not shown...
print('download wget: ', ' '.join([
    'cd .. && ',
    # 'curl -L -O ',
    # 'wget -O llama-2-13b-chat.ggmlv3.q2_K.bin',
    'wget --show-progress -O llama-2-13b-chat.ggmlv3.q2_K.bin',
    # 'https://www.google.com/'
    'https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/resolve/main/llama-2-13b-chat.ggmlv3.q2_K.bin'
]))
# stream_command_output(' '.join(), print=print)

# TODO: pip wget dependency:
# def download_file(url, out):
#     print(f"Downloading {url} to {out}")
#     wget.download(url, out=out)

# download_file('https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/resolve/main/llama-2-13b-chat.ggmlv3.q2_K.bin', 'llama-2-13b-chat.ggmlv3.q2_K.bin')

import urllib.request

def download_file(url, out):
    def show_progress(count, block_size, total_size):
        if count % 5_000 == 0:  # only print every hundred logs
            print(f"Downloaded {count*block_size} of {total_size}")

    print(f"Downloading {url} to {out}")
    urllib.request.urlretrieve(url, out, reporthook=show_progress)

download_file('https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/resolve/main/llama-2-13b-chat.ggmlv3.q2_K.bin', 'llama-2-13b-chat.ggmlv3.q2_K.bin')

# https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/resolve/main/llama-2-13b-chat.ggmlv3.q2_K.bin
print('make is not working right now')
# spawn_subprocess('cd llama.cpp && make')

time.sleep(100)