#!/usr/bin/env python3
from src.config import config, infraState
from src.spawn_subprocess import spawn_subprocess


def app__sync_head_n_local():
    # TODO:
    # its not so much smooth or easy to use... is current code right?
    # another options:
    # 1. use SSHFS for smooth development
    # 2. deploy over git repo

    print("=== downloading server modified source code and put it into my local git fs ===")
    
    source_1 = config.LOCAL_APP

    source_2 = f"{config.HEAD_NODE_USER}@{infraState.ip}:{config.HEAD_NODE_APP_SRC}"

    spawn_subprocess(' '.join([
        "rsync",
        "-az", 
        f'-e',
        f'"ssh -i {config.PEM_PATH}"',
        # '--delete',  # delete can't be there!
        source_1,
        source_2,
    ]))

    spawn_subprocess(' '.join([
        "rsync", "-az", 
        f'-e',
        f'"ssh -i {config.PEM_PATH}"',
        source_2,
        source_1,
    ]))


if __name__ == '__main__':
    app__sync_head_n_local()



