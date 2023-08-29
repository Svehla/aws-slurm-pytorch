import time
import subprocess
from src.head_node_ssh_communication import exec_sh_on_head_node
from src.config import config
from src.timer import format_seconds_duration

def get_batch_id_status(batch_id):
    output = exec_sh_on_head_node(f'squeue -j {str(batch_id)}', show_ssh_communication=False)

    lines = output.strip().split('\n')

    if len(lines) > 1:
        columns = lines[1].split()
        status = columns[4]
        return status
    else:
        return None


def expand_slurm_status_code(status_code):
    status_dict = {
        'R': 'Running',
        'PD': 'Pending',
        'S': 'Suspended',
        'CA': 'Cancelled',
        'CF': 'Configuring',
        'CG': 'Completing',
        'CD': 'Completed',
        'F': 'Failed',
        'TO': 'Timeout',
        'ST': 'Stopped',
        'NF': 'Node Failure',
        'RV': 'Revoked',
        'SE': 'Special Exit'
    }
    return status_dict.get(status_code, 'Unknown')

sinfo_desc = """
- `~`: Draining/Drained - Node not accepting new jobs.
- `#`: Mixed - Node partially used.
- `*`: Completing - Job finished, processes still active.
- `@`: Reserved - Node reserved for future use.
- `%`: Future - Node expected to be added.
- `$`: Power Save - Node powered down to save energy.
- `&`: Power Up - Node currently powering up.
"""

def watch_job_logs(batch_id):
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time
        time.sleep(3)
        logOut = []
        try:
            b_status = get_batch_id_status(batch_id)

            logOut.append(f"Elapsed time: {format_seconds_duration(elapsed_time)}")
            logOut.append(f"Batch id    : {batch_id}")
            logOut.append(f"Status      : {b_status} ({expand_slurm_status_code(b_status)})")

            if b_status == 'CF': # or pending state???? not sure
                logOut.append('~~~ waiting till all slurm nodes will be ready ~~~')
                sinfo = exec_sh_on_head_node("sinfo", show_ssh_communication=False)
                logOut.append(sinfo_desc)
                logOut.append(sinfo)
            else: 
                out = ''
                try:
                    out = exec_sh_on_head_node(f"cat {config.HEAD_NODE_APP_SRC}/../slurm_output/{batch_id}-slurm.out", show_ssh_communication=False)
                    logOut.append(f'batch output:')
                    logOut.append(f"=============")
                    logOut.append('')
                    logOut.append(out)
                except Exception as e:
                    logOut.append(f'slurm_output file for {batch_id} does not exist yet')
                    sinfo = exec_sh_on_head_node("sinfo", show_ssh_communication=False)
                    logOut.append(sinfo_desc)
                    logOut.append(sinfo)

                is_job_ended = exec_sh_on_head_node(f"squeue -h -j {batch_id}", show_ssh_communication=False)

                if len(is_job_ended) == 0:
                    subprocess.run('clear')
                    logOut.append('')
                    logOut.append('=== slurm batch is no more available ===')
                    print("\n".join(logOut))
                    break

        except Exception as e:
            logOut.append(f'e: {str(e)} ')
            print("\n".join(logOut))
            break

        subprocess.run('clear')
        print("\n".join(logOut))
