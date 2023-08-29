#!/usr/bin/env python
import subprocess
import time
from src.timer import format_seconds_duration

def create_colorize_func(color_code: str):
    def colorize(input_string: str) -> str:
        return f"\033[{color_code}m{input_string}\033[0m"
    return colorize

colorize_red = create_colorize_func("91")
colorize_gray = create_colorize_func("90")
colorize_blue = create_colorize_func("94")
colorize_yellow = create_colorize_func("93")
colorize_green = create_colorize_func("92")

# TODO: rewrite check_output with subprocess.Popen(...) to have continuous logs
# I want to have similar tooling for local spawn as for ssh-ing into HeadNode
def spawn_subprocess(cmd: str, show_cmd=True, show_time=True, show_out=True, print_prefix=''):

    if show_time:
        start_time = time.time()

    if show_cmd:
        print()
        print(colorize_gray(':~$ ') , colorize_yellow(cmd), sep='')

    process = subprocess.Popen(
        cmd,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout_output = []
    stderr_output = []

    for line in iter(process.stdout.readline, ''):
        line_decoded = line.strip()
        stdout_output.append(line_decoded)
        if show_out:
            print(colorize_blue(print_prefix), line_decoded, sep='')


    for line in iter(process.stderr.readline, ''):
        line_decoded = line.strip()

        # ------------------------------------------------------------
        # AAAAAARRRGHHHHHH Ignore the specific SSH warning message
        if "Warning: Permanently added" not in line_decoded:  
            stderr_output.append(line_decoded)
        else:
            print('HACK: stderr ssh Warning do not throw error !!!')

        if show_out:
            print(colorize_blue(print_prefix), line_decoded, sep='')
        # ------------------------------------------------------------

    stdout = '\n'.join(stdout_output)
    stderr = '\n'.join(stderr_output)

    if stderr:
        error_message = stderr
        raise Exception(f"cannot spawn subprocess error: \n{error_message}")

    if show_time:
        elapsed_time = time.time() - start_time
        print(colorize_gray(f"~took: {format_seconds_duration(elapsed_time)}"))

    return stdout


