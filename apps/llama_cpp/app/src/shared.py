# TODO: code duplicity!!!!

import sys
import subprocess

# do a shared library for /app_{i} with reused code +
# do a shared library for /app_{i}/ml_model with reused code

def create_colorize_func(color_code: str):
    def colorize(input_string: str) -> str:
        return f"\033[{color_code}m{input_string}\033[0m"
    return colorize

colorize_red = create_colorize_func("91")
colorize_gray = create_colorize_func("90")
colorize_blue = create_colorize_func("94")
colorize_yellow = create_colorize_func("93")
colorize_green = create_colorize_func("92")


og_print = print
def create_prefixed_print(log_prefix: str):
    def new_print(*args, **kwargs):
        if log_prefix and kwargs.get('end') != '':
            og_print(colorize_green(log_prefix), *args, **kwargs, flush=True) # flush is necessary!
        else:
            og_print(*args, **kwargs, flush=True) # flush is necessary!

    return new_print

print = create_prefixed_print('') # if print is not defined, we need to keep flush=True


import io

# TODO: unify exec/spawn subprocesses somehow
def stream_command_output(cmd, print=print):
    print()
    print(colorize_gray(':~$ ') , colorize_yellow(cmd), sep='')

    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def read_and_print(stream):
        output_str = ''
        while True:
            output = stream.read(1)
            if output == '' and process.poll() is not None:
                break
            if output != '':
                print(output, end='')
                output_str += output
        return output_str


    # without io wrapper i could not decode and print special utf-8 chars like: áé
    stdout = io.TextIOWrapper(process.stdout, encoding='utf-8')
    stderr = io.TextIOWrapper(process.stderr, encoding='utf-8')

    stdout_str = read_and_print(stdout)
    read_and_print(stderr)

    print('----------')
    print(stdout_str)

    process.stdout.close()
    process.stderr.close()
    process.wait()
    return stdout_str

def spawn_subprocess(cmd: str, show_cmd=True, show_out=True, print=print):
    if show_cmd:
        print()
        # print(colorize_yellow(f':~$ {cmd}'), sep='')
        print(colorize_gray(':~$ ') , colorize_yellow(cmd), sep='')
 
    # TODO: add continuous print via stream_command_output
    # output is shown when the job ended
    out = subprocess.check_output(cmd, text=True, shell=True)

    if show_out:
        if out and show_out:
            print(out)

    return out


def debug_identify_instance(print=print):
    import os
    if 'VIRTUAL_ENV' in os.environ:
        venv_path = os.environ['VIRTUAL_ENV']
        print(f"Virtual environment '{os.path.basename(venv_path)}' is active.")
    else:
        print("No virtual environment is active.")

    import requests
    response = requests.get('https://api.ipify.org?format=json')
    print('ip:', response.json()['ip'])
