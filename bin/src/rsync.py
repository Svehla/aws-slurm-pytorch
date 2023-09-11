#!/usr/bin/env python3
from src.config import config, infraState
from src.timer import format_seconds_duration
from src.spawn_subprocess import spawn_subprocess

def rsync_to_head_node(source_dir, TARGET_DIR):
    spawn_subprocess(' '.join([
        "rsync", "-az", 
        f'-e',
        f'"ssh -i {config.PEM_PATH}"',

        # it removes locally removed files
        # its good to keep the server clean, but it broke jupyter notebook experience
        # '--delete', 

        source_dir,
        f"{config.HEAD_NODE_USER}@{infraState.ip}:{TARGET_DIR}"
    ]))

