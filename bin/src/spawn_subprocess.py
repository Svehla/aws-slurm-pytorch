#!/usr/bin/env python
import subprocess
import time
from src.timer import format_seconds_duration

# TODO: rewrite check_output with subprocess.Popen(...) to have continuous logs
# I want to have similar tooling for local spawn as for ssh-ing into HeadNode
def spawn_subprocess(cmd: str, show_debug=True):
    if show_debug:
        start_time = time.time()
        print()
        print(':~$', cmd)

    out = subprocess.check_output(cmd, text=True, shell=True)

    if show_debug:
        if out:
            print(out)
        elapsed_time = time.time() - start_time
        print(f"~took: {format_seconds_duration(elapsed_time)}")
        print()

    return out


