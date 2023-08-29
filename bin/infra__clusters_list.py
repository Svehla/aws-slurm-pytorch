#!/usr/bin/env python
import json
from src.config import config
from src.cluster_state_utils import get_cluster_ip 
from src.timer import timer
from src.spawn_subprocess import spawn_subprocess

@timer
def list_clusters():

    print(f"available clusters for {config.REGION}:")

    output = spawn_subprocess(
        ' '.join(["pcluster", "list-clusters", '--region', config.REGION]),
        show_debug=False
    )
    
    clusters_info = json.loads(output)
    
    for index, cluster in enumerate(clusters_info['clusters']):
        ip_address = get_cluster_ip(config.REGION, cluster['clusterName'])
        print(f"{index + 1}) {cluster['clusterName']}, {cluster['clusterStatus']}, {cluster['scheduler']['type']}, IP: {ip_address}")
        print("\n")

list_clusters()