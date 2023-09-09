#!/usr/bin/env python3
from src.config import config, infraState
from src.spawn_subprocess import spawn_subprocess
from src.magic_shells import colorize_yellow, colorize_blue, colorize_gray
from src.before_connection import sh_before_connection
from src.array import filter_empty_items

# i may replace this with `shlex` library
def escape_bash_quotes(s):
    s = s.replace('\\', '\\\\') # this needs to be the replace line of this fn

    s = s.replace('`', '\\`')
    s = s.replace('$', '\\$')
    s = s.replace('"', '\\"')
    # it escapes single quotes. In bash, to insert a single quote into a single-quoted string, 
    #   we end the current string, insert an escaped single quote, and start a new string. 
    #   Hence, "'\\''" is used to insert a single quote.
    #   it's better to not to use ' in bash command if its not needed
    s = s.replace("'", "'\\''")
    return s




# target_source will be smth like ubuntu@{IP}
def cmd_over_ssh(target_source, pem_path, cmd, show_cmd=True, show_out=True, alias=''):
    print_prefix = f'[{alias if alias else target_source}]'

    sh_wrapped_command = ' '.join([
        'ssh', 
        # automatically add host into ~/.ssh/known_hosts
        '-o StrictHostKeyChecking=no',
        '-i', pem_path,
        target_source,
        # f'{config.HEAD_NODE_USER}@{infraState.ip}', 
        f''' 'bash -c "{escape_bash_quotes(cmd)}"' '''
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
    

def ssh_head_spawn_subprocess(cmd, activate_sources=True, show_cmd=True, show_out=True):
    init_command = ''
    if activate_sources:
        make_slurm_commands_available = 'source /etc/profile'
        # sh_before_connection
        init_command = ';'.join(filter_empty_items([make_slurm_commands_available, sh_before_connection])) + ';'

    if infraState.ip == None:
        raise Exception(f"infraState.ip is None, be sure that you have active pcluster")

    return cmd_over_ssh(
        f"{config.HEAD_NODE_USER}@{infraState.ip}",
        config.PEM_PATH,
        f'{init_command} {cmd}', show_cmd, show_out
    )


def ssh_compute_spawn_subprocess(node_id: str, cmd, show_out=False, show_cmd=False):
    return cmd_over_ssh(node_id, config.PEM_PATH, cmd, show_out, show_cmd)
