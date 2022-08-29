from os import environ

PROGRAM_PATH = f"{environ['APPDATA'] if 'APPDATA' in environ.keys() else environ['PROGRAMFILES']}\\OBA Otomatik Oynatici"
SETUP_PATH = f"{environ['TEMP']}\\OBA Setup"
TEMP_PATH = f"{environ['TEMP']}\\Oba Otomatik Oynatici"
LOG_PATH = f"{environ['TEMP']}\\OBA Log"
