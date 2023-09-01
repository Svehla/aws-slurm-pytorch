#!/usr/bin/env python
from src.config import config, infraState
from src.spawn_subprocess import spawn_subprocess
from src.colorize_shell import colorize_yellow, colorize_blue, colorize_gray

# i may replace this with `shlex` library
def escape_bash_quotes(s):
    s = s.replace('\\', '\\\\') # this needs to be the replace line of this fn

    s = s.replace('`', '\\`')
    s = s.replace('$', '\\$')
    s = s.replace('"', '\\"')
    # it escapes single quotes. In bash, to insert a single quote into a single-quoted string, 
    #   we end the current string, insert an escaped single quote, and start a new string. 
    #   Hence, "'\\''" is used to insert a single quote.
    s = s.replace("'", "'\\''")
    return s

def ssh_head_spawn_subprocess(cmd, activate_sources=True, show_cmd=True, show_out=True):
    init_command = ''

    if infraState.ip == None:
        raise Exception(f"infraState.ip is None, be sure that you have active pcluster")
        
    print_prefix = '[ssh->head]'

    if activate_sources:
        make_slurm_commands_available = 'source /etc/profile'
        # TODO: should i change sources by config? or keep only one source working?
        activate_venv = f'source /shared/{config.APP_DIR}/my-venv/bin/activate'
        init_command = f'{make_slurm_commands_available}; {activate_venv}; '

    sh_wrapped_command = ' '.join([
        'ssh', 
        # automatically add host into ~/.ssh/known_hosts
        '-o StrictHostKeyChecking=no',
        '-i', config.PEM_PATH,
        f'{config.HEAD_NODE_USER}@{infraState.ip}', 
        f''' 'bash -c "{escape_bash_quotes(f'{init_command} {cmd}')}"' '''
    ])

    if show_cmd:
        print()
        print(colorize_blue(f"{print_prefix}"), colorize_gray(':~$ '), colorize_yellow(cmd), sep='')

    
    out = spawn_subprocess(
        sh_wrapped_command,
        # show_cmd is override by custom show_cmd arg
        show_cmd=False,
        # show_cmd=True,
        show_out=show_out,
        show_time=show_cmd,
        # TODO: do we want to have prefix here?
        # print_prefix=print_prefix
    )
    return out
