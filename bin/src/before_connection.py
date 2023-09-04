from src.config import config
from pathlib import Path

def read_file(file_path):
    file_path = Path(file_path)
    if file_path.exists():
        return file_path.read_text()
    else:
        return None

sh_before_connection = read_file(
    f'{config.LOCAL_APP_SRC}/before_connection_config.template.sh'
).replace('{{APP_DIR}}', config.APP_DIR) \

# print('=== sh_before_connection ===')
# print(sh_before_connection)