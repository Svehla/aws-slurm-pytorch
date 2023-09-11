#!/usr/bin/env python3
from src.watch_sbatch_logs import watch_sbatch_logs
import time
    
def watch_sbatch(batch_id):
    start_time = time.time() # should start time be read from the slurm metadata?
    watch_sbatch_logs(batch_id, start_time=start_time)

def app__watch_sbatch():
    # TODO: should i store/read the latest slurm id?
    # 1. from catting slurm output files?
    # 2. bash magic: sbatch script.sh | awk '{print $4}' >> job_ids.log
    # 3. install sacct for slurm management
    job_id = 1337
    print(f'watching job {job_id}')
    watch_sbatch(job_id)

