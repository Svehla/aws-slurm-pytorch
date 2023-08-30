import time
import json
import subprocess
from datetime import datetime
from src.config import config
from src.timer import format_seconds_duration
from src.spawn_subprocess import spawn_subprocess

def show_cluster_status_progress():
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time
        cluster_info = spawn_subprocess(' '.join([
                "pcluster", "describe-cluster",
                "--cluster-name", config.CLUSTER_NAME,
                "--region", config.REGION
            ]), 
            show_out=False,
            show_cmd=False,
            show_time=False
        )
        cluster_info = json.loads(cluster_info)

        cluster_status = cluster_info.get('clusterStatus')

        if cluster_status == "CREATE_COMPLETE":
            print(f"{config.CLUSTER_NAME} is created.")
            break

        if cluster_status == "DELETE_COMPLETE":
            print(f"{config.CLUSTER_NAME} has been successfully deleted.")
            break

        subprocess.run('clear')
        print(f"Elapsed time     : {format_seconds_duration(elapsed_time)}")
        print(f"Cluster status   : {cluster_status}")
        creation_time = cluster_info.get('creationTime')

        print(f"Creation time    : {creation_time}")

        creation_timestamp = datetime.fromisoformat(creation_time.replace("Z", "")).timestamp()

        current_timestamp = datetime.utcnow().timestamp()
        duration = current_timestamp - creation_timestamp

        print(f"Till creation    : {format_seconds_duration(duration)}")

        time.sleep(3)