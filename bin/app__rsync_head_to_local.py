#!/usr/bin/env python3
from src.config import config, infraState
from src.spawn_subprocess import spawn_subprocess


def app__rsync_head_to_local():
    print("=== downloading server modified source code and put it into my local git fs ===")
    cmd = ' '.join([
        "rsync", "-az", 
        f'-e',
        f'"ssh -i {config.PEM_PATH}"',

        # it removes locally removed files
        # its good to keep the server clean, but it broke jupyter notebook experience
        # '--delete', 

        # from remote server
        f"{config.HEAD_NODE_USER}@{infraState.ip}:{config.HEAD_NODE_APP_SRC}",
        # download to local => it just replace .../app folder
        config.LOCAL_APP,
    ])
    # print(cmd)
    spawn_subprocess(cmd)


if __name__ == '__main__':
    app__rsync_head_to_local()



