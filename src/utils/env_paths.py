from os import environ

PROGRAM_PATH = f"{environ['PROGRAMFILES(x86)'] if 'PROGRAMFILES(x86)' in environ.keys() else environ['PROGRAMFILES']}\\OBA Otomatik Oynatici"
SETUP_PATH = f"{environ['TEMP']}\\OBA Setup"
TEMP_PATH = f"{environ['TEMP']}\\Oba Otomatik Oynatici"
