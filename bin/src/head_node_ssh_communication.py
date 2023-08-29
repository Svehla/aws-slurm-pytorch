#!/usr/bin/env python
import subprocess
from src.config import config, infraState
import time
from src.timer import format_seconds_duration

# escaping magic commands of commands hell, but I like it
def escape_quotes(s):
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace("'", "\\'")

    return s

# if you want to use 'activate_sources=True' you need to initialize new /venv before calling this fn
# TODO: parameters are weird, remove those output debugs and make it more logical and easier to user
def exec_sh_on_head_node(commands, activate_sources=True, pipe_output_to_print=False, show_ssh_communication=True):
    if not isinstance(commands, list):
        commands = [commands]

    out = ''

    # this function has no output => it could output array of outputs i guess?
    for comm in commands:
        start_time = time.time()
        out += exec_one_sh_on_head_node(
            comm,
            activate_sources=activate_sources,
            pipe_output_to_print=pipe_output_to_print,
            show_ssh_communication=show_ssh_communication, 
        )

        elapsed_time = time.time() - start_time
        if show_ssh_communication: 
            print(f"~took: {format_seconds_duration(elapsed_time)}")
            print()

    # no one use aggregated output functionality
    return out



def exec_one_sh_on_head_node(command, activate_sources=True, pipe_output_to_print=False, show_ssh_communication=True):
    init_command = ''

    if activate_sources:
        make_slurm_commands_available = 'source /etc/profile'
        # TODO: should i change sources by config? or keep only one source working?
        activate_venv = 'source /shared/ai_app/my-venv/bin/activate'
        init_command = f'{make_slurm_commands_available}; {activate_venv}; '

    sh_wrapped_command = ' '.join([
        'ssh', 
        # automatically add host into ~/.ssh/known_hosts
        '-o StrictHostKeyChecking=no',
        '-i', config.PEM_PATH,
        f'{config.HEAD_NODE_USER}@{infraState.ip}', 
        f''' 'bash -c "{escape_quotes(f'{init_command} {command}')}"' '''
    ])

    if show_ssh_communication:
        # print()
        # print('### run sh command over ssh:')
        # print('----------------------------')
        # print(f'local:~$ {sh_wrapped_command}')
        print()
        print(f"[head]:~$ {command}")

    # TODO: I'll prefer to call `spawn_subprocess.py` instead of custom spawning
    process = subprocess.Popen(sh_wrapped_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # we need to print output interactively
    stdout_output = []
    stderr_output = []

    # std python do not enable reading from stdout + stderr asynchronously by the server print order
    for line in iter(process.stdout.readline, b''):
        line_decoded = line.decode().strip()
        stdout_output.append(line_decoded)
        if pipe_output_to_print:
            print(line_decoded)


    for line in iter(process.stderr.readline, b''):
        line_decoded = line.decode().strip()

        # pay attention: ~/.ssh/known_hosts adding IP is warning is outputted into stderr
        # but its not error I do not want to throw app error
        if "Warning: Permanently added" not in line_decoded:  # Ignore the specific SSH warning message
            stderr_output.append(line_decoded)
        else:
            print('HACK: stderr ssh Warning do not throw error !!!')

        if pipe_output_to_print:
            print(line_decoded)

    stdout = '\n'.join(stdout_output)
    stderr = '\n'.join(stderr_output)

    if stderr:
        error_message = stderr
        raise Exception(f"HeadNode error occurred: \n{error_message}")


    return stdout
