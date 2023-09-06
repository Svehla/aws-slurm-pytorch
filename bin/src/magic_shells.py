
def create_colorize_func(color_code: str):
    def colorize(input_string: str) -> str:
        return f"\033[{color_code}m{input_string}\033[0m"
    return colorize

colorize_red = create_colorize_func("91")
colorize_gray = create_colorize_func("90")
colorize_blue = create_colorize_func("94")
colorize_yellow = create_colorize_func("93")
colorize_green = create_colorize_func("92")

# line wrapping is a new line, so this is not working :(
import sys
def clear_last_lines(n=1):
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    for _ in range(n):
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)
