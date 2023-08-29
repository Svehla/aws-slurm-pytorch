import subprocess

og_print = print
def create_prefixed_print(log_prefix: str):
    def new_print(*args, **kwargs):
        og_print(log_prefix, *args, **kwargs, flush=True) # flush is necessary!

    return new_print

print = create_prefixed_print('') # if print is not defined, we need to keep flush=True


# TODO: unify exec/spawn subprocesses somehow
def stream_command_output(cmd, print=print):
    print(':~$ ', cmd, sep='')
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for line in iter(process.stdout.readline, b''):
        print(line.decode(), end='')
    for line in iter(process.stderr.readline, b''):
        print(line.decode(), end='')
    process.stdout.close()
    process.stderr.close()
    process.wait()


def spawn_subprocess(cmd: str, show_debug=True, print_output=True, print=print):
    # import time
    if show_debug:
        # start_time = time.time()
        # print()
        print(':~$ ', cmd, sep='')
        print()

    # TODO: add continuous print via stream_command_output
    # output is shown when the job ended
    out = subprocess.check_output(cmd, text=True, shell=True)

    if show_debug:
        if out and print_output:
            print(out)
        # elapsed_time = time.time() - start_time
        # print(f"~took: {elapsed_time} sec")
        print()

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
    print('ip: ', response.json()['ip'])
