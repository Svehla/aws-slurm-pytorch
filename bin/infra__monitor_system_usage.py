#!/usr/bin/env python3
import time
import subprocess
from src.timer import format_seconds_duration
from src.ssh_head_spawn_subprocess import ssh_compute_spawn_subprocess
from src.compute_node import get_active_compute_nodes

# ------------------------ GPU section ------------------------

# TODO: alternatives:

# 1. create AWS dashboard via aws cli? + install plugin for GPU & RAM
# https://aws.amazon.com/blogs/machine-learning/monitoring-gpu-utilization-with-amazon-cloudwatch/
# sudo pip3 install nvidia-ml-py -y boto3
# connect to all compute nodes and run nvidia-smi on them

# 2. Pytorch profiler may analyze HW usage as well
#  https://pytorch.org/tutorials/recipes/recipes/profiler_recipe.html




def infra__monitor_system_usage():
    start_time = time.time()
    while True:
        # time.sleep(3)

        elapsed_time = time.time() - start_time
        logOut = []

        active_nodes = get_active_compute_nodes()

        logOut.append(f'elapsed {format_seconds_duration(elapsed_time)}')

        if len(active_nodes) == 0:
            logOut.append(f'no active nodes right now')

        # TODO: do those ssh in parallel via sub processes
        # one sync iteration for 1 node took ~11sec, without ssh overhead it took ~6sec
        for node in active_nodes:
            try:
                logOut.append('')
                logOut.append(f'-----{node["node"]}-----')

                all_usage = ssh_compute_spawn_subprocess(
                    node['node'], 
                    ' && '.join([
                        'echo;'
                        'nvidia-smi',
                        # TODO: call this in parallel and then merge it
                        # 'echo;'
                        # 'df -h',
                        # 'echo;'
                        # 'free -h',
                        # 'echo;'
                        # 'top -b -n 1 | grep "Cpu(s)"'
                    ])
                )
                logOut.append(all_usage)
                logOut.append('')

                # TODO: do those ssh in parallel via sub processes
                """
                disk_usage = ssh_compute_spawn_subprocess(node['node'], 'nvidia-smi')
                disk_usage = ssh_compute_spawn_subprocess(node['node'], 'df -h')
                ram_usage = ssh_compute_spawn_subprocess(node['node'], 'free -h')
                cpu_usage = ssh_compute_spawn_subprocess(node['node'], 'top -b -n 1 | grep "Cpu(s)"')
                logOut.append(gpu_usage)
                logOut.append('')
                logOut.append(cpu_usage)
                logOut.append('')
                logOut.append(disk_usage)
                logOut.append('')
                logOut.append(ram_usage)
                """
            except Exception as e:
                logOut.append(f"some err occurred: {e}")


        subprocess.run('clear')
        print("\n".join(logOut))




if __name__ == "__main__":
    infra__monitor_system_usage()