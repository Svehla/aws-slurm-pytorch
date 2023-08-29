#!/usr/bin/env python
import subprocess
from src.cluster_status import show_cluster_status_progress
from src.cluster_state_utils import invalidate_ip_cache
from src.config import config
from src.timer import timer

# took ~6-7-9min
@timer
def delete_cluster():
    try: 
        invalidate_ip_cache()
        command = [
            "pcluster",
            "delete-cluster",
            "--cluster-name",
            config.CLUSTER_NAME,
            "--region",
            config.REGION,
        ]

        subprocess.run(command, check=True, text=True)

        show_cluster_status_progress()

    except Exception as e:
        print(f"An error occurred:")
        print(e)

delete_cluster()