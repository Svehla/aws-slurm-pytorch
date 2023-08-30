import time
import subprocess
from src.ssh_head_spawn_subprocess import ssh_head_spawn_subprocess
from src.config import config
from src.timer import format_seconds_duration
from src.colorize_shell import colorize_gray

def get_batch_id_status(batch_id):
    output = ssh_head_spawn_subprocess(f'squeue -j {str(batch_id)}', show_cmd=False, show_out=False)

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

def watch_job_logs(batch_id, start_time = time.time()):
    while True:
        elapsed_time = time.time() - start_time
        time.sleep(1)
        logOut = []
        try:
            b_status = get_batch_id_status(batch_id)

            logOut.append(f"time     : {format_seconds_duration(elapsed_time)}")
            logOut.append(f"Batch id : {batch_id}")
            logOut.append(f"Status   : {b_status} ({expand_slurm_status_code(b_status)})")

            if b_status == 'CF': # or pending state???? not sure
                logOut.append('~~~ waiting till all slurm nodes will be ready ~~~')
                sinfo = ssh_head_spawn_subprocess("sinfo", show_cmd=False, show_out=False)
                logOut.append(sinfo_desc)
                logOut.append(sinfo)
            else: 
                out = ''
                try:
                    out = ssh_head_spawn_subprocess(f"cat {config.HEAD_NODE_APP_SRC}/../slurm_output/{batch_id}-slurm.out", show_cmd=False, show_out=False)
                    logOut.append("================= batch output =================")

                    logOut = [colorize_gray(item) for item in logOut]
                    logOut.append('')
                    logOut.append(out)
                except Exception as e:
                    logOut.append(f'slurm_output file for {batch_id} does not exist yet')
                    sinfo = ssh_head_spawn_subprocess("sinfo", show_cmd=False, show_out=False)
                    logOut.append(sinfo_desc)
                    logOut.append(sinfo)

                is_job_ended = ssh_head_spawn_subprocess(f"squeue -h -j {batch_id}", show_cmd=False, show_out=False)

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

