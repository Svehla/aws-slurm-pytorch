# TODO: code duplicity!!!!

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
        if log_prefix:
            og_print(colorize_green(log_prefix), *args, **kwargs, flush=True) # flush is necessary!
        else:
            og_print(*args, **kwargs, flush=True) # flush is necessary!

    return new_print

print = create_prefixed_print('') # if print is not defined, we need to keep flush=True


# TODO: unify exec/spawn subprocesses somehow
def stream_command_output(cmd, print=print):
    print()
    print(colorize_gray(':~$ ') , colorize_yellow(cmd), sep='')
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # line reading...
    for line in iter(process.stdout.readline, b''):
        print(line.decode(), end='')
    for line in iter(process.stderr.readline, b''):
        print(line.decode(), end='')

    # char reading
    while process.poll() is None:
        stdout = process.stdout.read(1).decode()
        if stdout:
            print(stdout, end='', flush=True)
        stderr = process.stderr.read(1).decode()
        if stderr:
            print(stderr, end='', flush=True)

    process.stdout.close()
    process.stderr.close()
    process.wait()


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
