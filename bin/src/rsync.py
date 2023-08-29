#!/usr/bin/env python
from src.config import config, infraState
from src.timer import format_seconds_duration
from src.spawn_subprocess import spawn_subprocess

def rsync_to_head_node(source_dir, TARGET_DIR):
    command = ' '.join([
        "rsync", "-az", 
        f'-e',
        f'"ssh -i {config.PEM_PATH}"',
        '--delete', # it removes locally removed files
        source_dir,
        f"{config.HEAD_NODE_USER}@{infraState.ip}:{TARGET_DIR}"
    ])

    spawn_subprocess(command)

