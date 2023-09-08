#!/usr/bin/env python3
import subprocess
import time
from src.timer import format_seconds_duration
from src.magic_shells import colorize_yellow, colorize_gray, colorize_blue, colorize_red

# TODO: apply char streams, not line streams
# def stream_command_output(cmd, print=print):
#     print()
#     print(colorize_gray(':~$ ') , colorize_yellow(cmd), sep='')

#     process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # def read_and_print(stream):
    #     output_str = ''
    #     while True:
    #         output = stream.read(1)
    #         if output == '' and process.poll() is not None:
    #             break
    #         if output != '':
    #             print(output, end='')
    #             output_str += output
    #     return output_str


    # # without io wrapper i could not decode and print special utf-8 chars like: áé
    # stdout = io.TextIOWrapper(process.stdout, encoding='utf-8')
    # stderr = io.TextIOWrapper(process.stderr, encoding='utf-8')

#     stdout_str = read_and_print(stdout)
#     read_and_print(stderr)

#     print('----------')
#     print(stdout_str)

#     process.stdout.close()
#     process.stderr.close()
#     process.wait()
#     return stdout_str

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

"""
# TODO: Fix streaming tokens and lines and make it elegant somehow


import sys
import io
import time
import subprocess
import time

def spawn_subprocess(cmd: str, show_cmd=True, show_time=True, show_out=True, print_prefix=''):
    if show_time:
        start_time = time.time()

    if show_cmd:
        print()
        print(colorize_gray(':~$ ') , colorize_yellow(cmd), sep='')

    process = subprocess.Popen(
        cmd,
        shell=True,
        # nice piping output 
        stdout=sys.stdout,
        # stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    # process.wait()

    # stdout_output = ""
    # stderr_output = ""

    # stdout_wrapper = io.TextIOWrapper(process.stdout, encoding='utf-8')
    # stderr_wrapper = io.TextIOWrapper(process.stderr, encoding='utf-8')

    # Initialize a variable to keep track of whether we're inside an escape sequence
    # support colors token streams
    
    # ----
    # def process_stream(stream, print_prefix, show_out):
    #     wrapper = io.TextIOWrapper(stream, encoding='utf-8')

    #     # Initialize a variable to keep track of whether we're inside an escape sequence
    #     inside_escape_sequence = False
    #     escape_sequence = ''
    #     output = ''

    #     for char in iter(lambda: wrapper.read(1), ''):
    #         if char == '\033':
    #             # We've encountered the start of an escape sequence
    #             inside_escape_sequence = True
    #             escape_sequence += char
    #         elif inside_escape_sequence:
    #             # We're inside an escape sequence, so add the character to the escape sequence string
    #             escape_sequence += char
    #             if escape_sequence.endswith('\033[0m'):
    #                 # We've encountered the end of the escape sequence
    #                 print(escape_sequence, end='')  # Print the escape sequence directly
    #                 inside_escape_sequence = False
    #                 escape_sequence = ''
    #         else:
    #             output += char
    #             if show_out: 
    #                 print(colorize_blue(print_prefix), char, sep='', end='')
    #                 time.sleep(0.01)
    #     return output

    # # Use the function to process the stdout and stderr streams
    # stdout_output = process_stream(process.stdout, print_prefix, show_out)
    # stderr_output = process_stream(process.stderr, print_prefix, show_out)


    if "Warning: Permanently added" in stderr_output:
        print(colorize_red('HACK: stderr ssh Warning do not throw error !!!'))
        stderr_output = stderr_output.replace("Warning: Permanently added", "")

    if stderr_output:
        error_message = stderr_output
        raise Exception(f"cannot spawn subprocess error: \n{error_message}")

    if show_time:
        elapsed_time = time.time() - start_time
        print(colorize_gray(f"~took: {format_seconds_duration(elapsed_time)}"))

    # print(stdout_output)
    # return stdout_output
"""