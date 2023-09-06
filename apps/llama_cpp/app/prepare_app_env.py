#!/usr/bin/env python3


# TODO: create python modules to fix it somehow
import sys
sys.path.append('/shared/llama_cpp/app') # fix shared import

from src.shared import create_prefixed_print, spawn_subprocess, stream_command_output
import time
import os

# TODO: resolve jump host log output for downloading of LLM models somehow
# import wget
# run llama locally on ubuntu:
# https://replicate.com/blog/run-llama-locally
# TODO: should it be run from head node, or compute node?

print = create_prefixed_print('[llama.cpp->prepare_app_env]') 


# TODO: download cuda toolkit
# full cuda driver is not available
# An instance with an attached NVIDIA GPU, such as a P3 or G4dn instance,
# must have the appropriate NVIDIA driver installed. Depending on the instance type,
# you can either download a public NVIDIA driver, download a driver from
# Amazon S3 that is available only to AWS customers, or use an AMI with the
# driver pre-installed.
# > https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/install-nvidia-driver.html

"""
asd attach_to_compute_node
# TODO: create some AI AMI with pre-installed libs
sudo apt update
sudo apt install nvidia-cuda-toolkit 
"""
# TODO: create AMI with preinstalled packages
spawn_subprocess("sudo apt-get update")
spawn_subprocess("sudo DEBIAN_FRONTEND=noninteractive apt-get install -y nvidia-cuda-toolkit") # install cuda drivers
spawn_subprocess("nvcc --version")

repo_url = "https://github.com/ggerganov/llama.cpp"
local_path = "llama.cpp"

is_cloned = os.path.exists(f'../{local_path}')


spawn_subprocess("pwd")

if not is_cloned:
    # Repo does not exist locally, clone it
    spawn_subprocess(f'cd .. && git clone {repo_url} {local_path}', print=print)
else:
    # Repo exists locally, update it
    spawn_subprocess(f'cd .. && git -C {local_path} pull', print=print)


stream_command_output(' '.join([
    'cd .. &&',
    'cd llama.cpp &&',
    # cublas enable nvidia usage 
    'make clean &&',

    # if i run this command multiple times, make will broke compiled output... weird
    # TODO: if i add support for GPU, main file is missing...
    # 'make -j',
    # need to fix path: https://github.com/ggerganov/llama.cpp/issues/1404 to make nvcc works
    'PATH="/usr/local/cuda/bin/:$PATH" LLAMA_CUBLAS=1 make'
]), print=print)

# === downloading dataset should be in the different module, not prepare_app_env ===
# TODO: download LLama weights

# TODO: build via make LLAMA_CUBLAS=1?
# https://dev.to/timesurgelabs/how-to-run-llama-2-on-anything-3o5m

"""
# downloading do not respond right now...
# it looks that wget/curl do not return new line, so the progress bar is not shown...
print('download wget: ', ' '.join([
    'cd .. && cd models && ',
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

"""
# ---------------------------------------------------------------


"""
# download via raw python
import urllib.request

def download_file(url, out):
    def show_progress(count, block_size, total_size):
        if count % 5_000 == 0:  # only print every hundred logs
            print(f"Downloaded {count*block_size} of {total_size}")

    print(f"Downloading {url} to {out}")
    urllib.request.urlretrieve(url, out, reporthook=show_progress)

download_file('https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/resolve/main/llama-2-13b-chat.ggmlv3.q2_K.bin', 'llama-2-13b-chat.ggmlv3.q2_K.bin')
"""

"""
mkdir models
cd models
wget https://huggingface.co/substratusai/Llama-2-13B-chat-GGUF/resolve/main/model.bin -O model.q4_k_s.gguf
"""


spawn_subprocess('mkdir -p ../models', print=print)
"""
import time

"""
# Data preparation should be in another script i guess

print("")
print("-----------------------")
print("USER ACTION REQUIRED!!!")
download_wget_cmd =' '.join([
    'cd .. && cd models && ',
    # 'curl -L -O  https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/resolve/main/llama-2-13b-chat.ggmlv3.q2_K.bin'

    # only one working solution i guess...???
    "wget https://huggingface.co/substratusai/Llama-2-13B-chat-GGUF/resolve/main/model.bin"

    # ???
    # "wget https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/blob/main/llama-2-13b-chat.ggmlv3.q3_K_M.bin"

    # available models:
    # > https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/tree/main
    "wget https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/resolve/main/llama-2-13b-chat.ggmlv3.q3_K_M.bin"

    # llama.cpp readme source: 
    # https://huggingface.co/openlm-research/open_llama_13b
    "wget https://huggingface.co/openlm-research/open_llama_13b/resolve/main/pytorch_model-00001-of-00003.bin" 
])
print("")
print("-----------------------")
print("")
# stream_command_output(download_wget_cmd)
print(download_wget_cmd)

# https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/resolve/main/llama-2-13b-chat.ggmlv3.q2_K.bin
