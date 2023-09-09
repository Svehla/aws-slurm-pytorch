#!/usr/bin/env python3
import time
import subprocess
from src.timer import format_seconds_duration
from src.ssh_spawn_subprocess import ssh_compute_spawn_subprocess
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
        log_out = []

        active_nodes = get_active_compute_nodes()

        log_out.append(f'elapsed {format_seconds_duration(elapsed_time)}')

        if len(active_nodes) == 0:
            log_out.append(f'no active nodes right now')

        # TODO: do those ssh in parallel via sub processes
        # one sync iteration for 1 node took ~11sec, without ssh overhead it took ~6sec
        for node in active_nodes:
            try:
                log_out.append('')
                log_out.append(f'-----{node["node"]}-----')


                # TODO: very very fast hack to have fast almost realtime GPU usage
                all_usage = ssh_compute_spawn_subprocess(
                    node['node'],
                    'while true; do clear; nvidia-smi; sleep 0.2; done',
                    show_out=True
                )
                # 'while true; do clear; nvidia-smi; sleep 0.2; done',
                """
                all_usage = ssh_compute_spawn_subprocess(
                    node['node'], 
                    ' && '.join([
                        # 'echo;'
                        # 'nvidia-smi',
                        # TODO: call this in parallel and then merge it
                        # 'echo;'
                        # 'df -h',
                        # 'echo;'
                        # 'free -h',
                        # 'echo;'
                        # 'top -b -n 1 | grep "Cpu(s)"'
                    ])
                )
                """
                log_out.append(all_usage)
                log_out.append('')

                # TODO: do those ssh in parallel via sub processes
                """
                disk_usage = ssh_compute_spawn_subprocess(node['node'], 'nvidia-smi')
                disk_usage = ssh_compute_spawn_subprocess(node['node'], 'df -h')
                ram_usage = ssh_compute_spawn_subprocess(node['node'], 'free -h')
                cpu_usage = ssh_compute_spawn_subprocess(node['node'], 'top -b -n 1 | grep "Cpu(s)"')
                log_out.append(gpu_usage)
                log_out.append('')
                log_out.append(cpu_usage)
                log_out.append('')
                log_out.append(disk_usage)
                log_out.append('')
                log_out.append(ram_usage)
                """
            except Exception as e:
                log_out.append(f"some err occurred: {e}")


        subprocess.run('clear')
        print("\n".join(log_out))




if __name__ == "__main__":
    infra__monitor_system_usage()