import time
from functools import wraps
from src.colorize_shell import colorize_gray

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(colorize_gray(f"function: '{func.__name__}' took: {format_seconds_duration(execution_time)}"))
        print()
        return result
    return wrapper

def format_seconds_duration(elapsed_time):
    elapsed_time = round(elapsed_time, 1)
    hours = elapsed_time // 3600
    minutes = (elapsed_time % 3600) // 60
    seconds = round(elapsed_time % 60, 1)

    if elapsed_time < 60:
        return f"{seconds} seconds"
    elif elapsed_time < 3600:
        return f"{minutes} minutes {seconds} seconds"
    else:
        return f"{hours} hours {minutes} minutes {seconds} seconds"