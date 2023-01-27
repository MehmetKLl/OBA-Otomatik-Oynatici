from os import environ

VERSION = "1.4.3"

class File:
    PROGRAM_PATH = f"{environ['APPDATA']}\\OBA Otomatik Oynatici"
    TEMP_PATH = f"{environ['TEMP']}\\Oba Otomatik Oynatici"
    LOG_PATH = f"{environ['TEMP']}\\OBA Log"

class Registry:
    KEY_PATH = "SOFTWARE\\OBA Otomatik Oynatici"

    VERSION_FULL_KEY_PATH = "HKEY_CURRENT_USER\\SOFTWARE\\OBA Otomatik Oynatici\\version"
    VERSION_KEY_NAME = "version"

    LASTCRASH_FULL_KEY_PATH = "HKEY_CURRENT_USER\\SOFTWARE\\OBA Otomatik Oynatici\\LastCrash"
    LASTCRASH_KEY_NAME = "LastCrash"

class GitHub:
    VERSION_URL = "https://raw.githubusercontent.com/MehmetKLl/OBA-Otomatik-Oynatici/main/src/VERSION"
    EXECUTABLE_URL = "https://github.com/MehmetKLl/OBA-Otomatik-Oynatici/raw/main/src/executable/x86.zip"

class Player:
    SCROLL_DELAY = 1
    VIDEO_CHECK_DELAY = 5
    SCROLL_VALUE = -100

class InstallerDialogs:
    TITLE = "ÖBA Otomatik Oynatıcı"
    UPDATER_TITLE = f"{TITLE} | Güncelleme Sistemi"
    INSTALLER_TITLE = f"{TITLE} | Kurulum"
    TROUBLESHOOTER_TITLE = f"{TITLE} | Otomatik Tamir Sistemi"

class GUI:
    TITLE = f"ÖBA Otomatik Oynatıcı v{VERSION}"
    SHORTCUT = "ALT+Z"
    DEV_MODE = False
    AUTOCLOSE = True

