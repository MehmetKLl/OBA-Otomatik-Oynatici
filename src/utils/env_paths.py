from os import environ

PROGRAM_PATH = f"{environ['APPDATA']}\\OBA Otomatik Oynatici"
TEMP_PATH = f"{environ['TEMP']}\\Oba Otomatik Oynatici"
LOG_PATH = f"{environ['TEMP']}\\OBA Log"
KEY_PATH = "SOFTWARE\\OBA Otomatik Oynatici"
FULL_KEY_PATH = "HKEY_CURRENT_USER\\SOFTWARE\\OBA Otomatik Oynatici\\version"
KEY_NAME = "version"
