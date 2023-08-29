#!/usr/bin/env python
from src.config import config, infraState
from src.spawn_subprocess import spawn_subprocess, colorize_yellow, colorize_blue, colorize_gray

# escaping magic commands of commands hell, but I like it
def escape_quotes(s):
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace("'", "\\'")
    return s

def exec_sh_on_head_node(cmd, activate_sources=True, show_out=False, show_ssh_communication=True):
    init_command = ''

    print_prefix = '[ssh->head]'

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
        f''' 'bash -c "{escape_quotes(f'{init_command} {cmd}')}"' '''
    ])

    if show_ssh_communication:
        print()
        print(colorize_blue(f"{print_prefix}"), colorize_gray(':~$ '), colorize_yellow(cmd), sep='')

    
    out = spawn_subprocess(
        sh_wrapped_command,
        # show_cmd is override by custom show_ssh_communication arg
        show_cmd=False,
        show_out=show_out,
        show_time=show_ssh_communication,
        # TODO: do we want to have prefix here?
        # print_prefix=print_prefix
    )
    return out
