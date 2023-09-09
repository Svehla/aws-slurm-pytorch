import time
from src.timer import format_seconds_duration
import subprocess

# TODO: use this function more in the codebase + do proper testing
def monitor_progress(callback, check_interval=3, start_time=time.time()):
    # print('Start monitoring progress...')
    # is_init = True

    def append_print(log):
        log_out.append(log)

    while True:
        time.sleep(3)
        elapsed_time = time.time() - start_time
        log_out = []


        should_end = callback(append_print)
        if should_end == True:
            return None

        # print(f'Elapsed {format_seconds_duration(elapsed_time)}, status: {status}')
        log_out.insert(0, f'elapsed {format_seconds_duration(elapsed_time)}')

        subprocess.run('clear')
        print("\n".join(log_out))

        time.sleep(check_interval)