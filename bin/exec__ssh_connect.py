#!/usr/bin/env python

import os
from src.config import config

def run_pcluster():
    # exec vector path => execvp
    os.execvp("pcluster", [
        "pcluster", "ssh", 
        # add host automatically into ~/.ssh/known_hosts
        '-o StrictHostKeyChecking=no',
        "--cluster-name", config.CLUSTER_NAME, 
        "-i", 
        config.PEM_PATH,
    ])

run_pcluster()