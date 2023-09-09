import time
import subprocess
from src.ssh_spawn_subprocess import ssh_head_spawn_subprocess
from src.config import config
from src.timer import format_seconds_duration
from src.magic_shells import colorize_gray, clear_last_lines

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
    log_out = []
    prev_log_out_len = 0

    def print_log_out():
        nonlocal log_out
        nonlocal prev_log_out_len
        # this is not working if line is automatically break into 
        # multiple line if its too long to be shown
        # mmm what to do with it???
        clear_last_lines(prev_log_out_len)
        subprocess.run('clear')
        output_to_print = "\n".join(log_out)
        print(output_to_print)
        # print('should remove', prev_log_out_len, 'lines', log_out)
        prev_log_out_len = output_to_print.count('\n') + 1
        # prev_log_out_len = len(output_to_print.split('\n'))
        log_out = []

    while True:
        elapsed_time = time.time() - start_time
        time.sleep(1)
        try:
            b_status = get_batch_id_status(batch_id)

            log_out.append('')
            log_out.append(f"time     : {format_seconds_duration(elapsed_time)}")
            log_out.append(f"Batch id : {batch_id}")
            log_out.append(f"Status   : {b_status} ({expand_slurm_status_code(b_status)})")

            if b_status == 'CF': # or pending state???? not sure
                log_out.append('~~~ waiting till all slurm nodes will be ready ~~~')
                sinfo = ssh_head_spawn_subprocess("sinfo", show_cmd=False, show_out=False)
                log_out.append(sinfo_desc)
                log_out.append(sinfo)   
            else: 
                out = ''
                try:
                    log_out.append("================= sbatch =================")

                    # I should open ssh and stream file to the terminal like: `tail -f`
                    is_job_ended = ssh_head_spawn_subprocess(f"squeue -h -j {batch_id}", show_cmd=False, show_out=False)

                    out = ssh_head_spawn_subprocess(f"cat {config.HEAD_NODE_APP}/slurm_output/{batch_id}-slurm.out", show_cmd=False, show_out=False)

                    log_out = [colorize_gray(item) for item in log_out]
                    log_out.append('')
                    log_out.append(out)

                    if len(is_job_ended) == 0:
                        log_out.append('')
                        log_out.append('=== slurm batch is no more available ===')
                        print_log_out()
                        break
                except Exception as e:
                    log_out.append(f'slurm_output file for {batch_id} does not exist yet')
                    sinfo = ssh_head_spawn_subprocess("sinfo", show_cmd=False, show_out=False)
                    log_out.append(sinfo_desc)
                    log_out.append(sinfo)

        except Exception as e:
            log_out.append(f'e: {str(e)} ')
            print_log_out()
            break

        print_log_out()
