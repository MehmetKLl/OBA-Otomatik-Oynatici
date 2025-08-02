from os import environ

VERSION = "1.5.0"

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

    FIRSTUSE_FULL_KEY_PATH = "HKEY_CURRENT_USER\\SOFTWARE\\OBA Otomatik Oynatici\\FirstUse"
    FIRSTUSE_KEY_NAME = "FirstUse"

class GitHub:
    VERSION_URL = "https://raw.githubusercontent.com/MehmetKLl/OBA-Otomatik-Oynatici/main/src/VERSION"
    EXECUTABLE_URL = "https://github.com/MehmetKLl/OBA-Otomatik-Oynatici/raw/main/src/executable/x86.zip" 
    SUPPORT_ME_URL = "https://github.com/MehmetKLl/OBA-Otomatik-Oynatici#beni-desteklemek-i%C3%A7in"               
    
class Player:
    SCROLL_DELAY = 1
    VIDEO_CHECK_DELAY = 5
    BORDER_CHECK_DELAY = 1
    PAGE_LOADING_DELAY = 10
    SCROLL_VALUE = -100

class InstallerDialogs:
    TITLE = "ÖBA Otomatik Oynatıcı"
    UPDATER_TITLE = f"{TITLE} | Güncelleme Sistemi"
    INSTALLER_TITLE = f"{TITLE} | Kurulum"
    TROUBLESHOOTER_TITLE = f"{TITLE} | Otomatik Tamir Sistemi"
    LICENSE_TITLE = f"{TITLE} | Lisans Sözleşmesi"

class GUI:
    TITLE = f"ÖBA Otomatik Oynatıcı v{VERSION}"
    SHORTCUT = "ALT+Z"
    DEV_MODE = False
    AUTOCLOSE = True

    TUTORIAL_TEXT = ("Uygulamayı kullanmadan önce;<br><br>" +
                     "<b>•</b> <b><i>Program videoların izlendiği kısımdan itibaren başlatılmalıdır (Site boyutu %100 olmak şartıyla)</i></b>. Aksi takdirde program doğru <b>çalışmayacaktır</b>.<br>" +
                     "<b>•</b> Uygulama çalışırken ekranda <b><i>sadece ÖBA'nın açık olduğu tarayıcı</i></b> açık olmalıdır.<br>" +
                     "<b>•</b> <b><i>Program çalışırken fare ile oynanmamalı</i></b> ve program durdurulmak isteniyorsa <b><i>sadece kısayol tuşuyla kapatılmalıdır</ins></b>, aksi takdirde program çökebilir, beklenmedik biçimde çalışabilir veya uygulama koordinat bazlı görüntü işleme algoritması ile çalıştığı için <b>tamamen işlevsiz hale gelebilir</b>.<br><br><br>"+
                     f"Uygulamanın varsayılan durdurma tuş kombinasyonu <b><i>{SHORTCUT}</i></b>'dir. Bu kombinasyonu ayarlar sekmesinden değiştirebilirsiniz.")