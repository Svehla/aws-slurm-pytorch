#!/usr/bin/env python
from src.cluster_status import show_cluster_status_progress
from src.cluster_state_utils import invalidate_ip_cache
from src.config import config
from src.timer import timer
from src.spawn_subprocess import spawn_subprocess

# took ~6-7-9min
@timer
def infra__cluster_delete():
    try: 
        invalidate_ip_cache()
        spawn_subprocess(' '.join([
            "pcluster",
            "delete-cluster",
            "--cluster-name",
            config.CLUSTER_NAME,
            "--region",
            config.REGION,
        ]))

        show_cluster_status_progress()

    except Exception as e:
        print(f"An error occurred:")
        print(e)


if __name__ == "__main__":
    infra__cluster_delete()