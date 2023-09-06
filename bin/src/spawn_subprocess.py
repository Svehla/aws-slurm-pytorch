#!/usr/bin/env python3
import subprocess
import time
from src.timer import format_seconds_duration
from src.magic_shells import colorize_yellow, colorize_gray, colorize_blue, colorize_red

# TODO: rewrite check_output with subprocess.Popen(...) to have continuous logs
# I want to have similar tooling for local spawn as for ssh-ing into HeadNode
# TODO: is it correct name of the function?
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

    # TODO: should i print it over chars, not lines? similar as llama shared utils stream?
    for line in iter(process.stdout.readline, ''):
        line_decoded = line.rstrip('\n')
        stdout_output.append(line_decoded)
        if show_out:
            print(colorize_blue(print_prefix), line_decoded, sep='')


    for line in iter(process.stderr.readline, ''):
        line_decoded = line.rstrip('\n')

        # ------------------------------------------------------------
        # AAAAAARRRGHHHHHH Ignore the specific SSH warning message
        if "Warning: Permanently added" not in line_decoded:  
            stderr_output.append(line_decoded)
            if show_out:
                print(colorize_blue(print_prefix), line_decoded, sep='')
        else:
            # if show_out:
            print(colorize_red('HACK: stderr ssh Warning do not throw error !!!'))
            # print(colorize_red('HACK: stderr ssh Warning do not throw error !!!\n' + line_decoded))

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


