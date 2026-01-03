from os import environ

VERSION = "1.6.0"

class File:
    PROGRAM_PATH = f"{environ['APPDATA']}\\OBA Otomatik Oynatici"
    TEMP_PATH = f"{environ['TEMP']}\\Oba Otomatik Oynatici"
    LOG_PATH = f"{environ['TEMP']}\\OBA Log"
    STUB_PATH = f"{environ['TEMP']}\\oba_otomatik_oynatma_stub"

class Registry:
    FULL_KEY_PATH = "HKEY_CURRENT_USER\\SOFTWARE\\OBA Otomatik Oynatici"
    KEY_PATH = "SOFTWARE\\OBA Otomatik Oynatici"

    VERSION_FULL_KEY_PATH = "HKEY_CURRENT_USER\\SOFTWARE\\OBA Otomatik Oynatici\\version"
    VERSION_KEY_NAME = "version"

    LASTCRASH_FULL_KEY_PATH = "HKEY_CURRENT_USER\\SOFTWARE\\OBA Otomatik Oynatici\\LastCrash"
    LASTCRASH_KEY_NAME = "LastCrash"

    FIRSTUSE_FULL_KEY_PATH = "HKEY_CURRENT_USER\\SOFTWARE\\OBA Otomatik Oynatici\\FirstUse"
    FIRSTUSE_KEY_NAME = "FirstUse"

class GitHub:
    LATEST_RELEASE_URL = "https://api.github.com/repos/MehmetKLl/OBA-Otomatik-Oynatici/releases/latest"
    FEEDBACK_URL = "https://forms.gle/6o3kqXHRJ2iXEqs36"               
    
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
    STUB_TITLE = f"{TITLE} | Uyumluluk Yöneticisi"
    LICENSE_TITLE = f"{TITLE} | Lisans Sözleşmesi"

    LICENSE_TEXT = ("ÖBA Otomatik Oynatıcı, çalıştırdığınız dosyanın sürümü itibariyle GNU GPLv3 lisansı altındadır ve olduğu gibi size sunulmaktadır. Geliştirici doğabilecek zararlarda ya da kötü durumlarda hiçbir sorumluluk kabul etmez. Aynı zamanda, bu yazılım açık kaynaktır ve kodları özgürce kullanılabilir ama işbu lisans gereği bu programın kodlarını kullanan diğer yazılımlar da aynı lisansı kullanmak, telif hakkı bildirimi ve kaynak kodlarını açık tutma yükümlülüğüne sahiptir.\n" +
                    f"(https://github.com/MehmetKLl/OBA-Otomatik-Oynatici/blob/main/LICENSE)\n\n" +
                    "Lisansın koşullarını kabul edip programı cihazınıza kurmak istiyor musunuz?")

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
    
    FEEDBACK_TEXT = ("<i>Kullanımınız nasıldı?</i><br><br>"+
                     "Projenin en başından beri <i>var oluş amacı</i> <b><i>güvenilirliğini</i></b> ortaya koyarak bir güven ortamı oluşturmak ve kullanıcılarının hiçbir <b><i>teknik bilgiye gerek kalmadan</i></b> kolayca işini halletmesiydi. Lakin projenin bağımsız bir biçimde bu ilkeler doğrultusunda geliştirilmesi <i>gerekli acil yamaların geç gelmesi</i>, <i>bazı hataların maalesef erken fark edilememesi</i> gibi <i>sorunlara</i> <b>sebep oluyor</b> ve <u><i>muazzam bir bakım yükünü</i></u> de <b>beraberinde getiriyor</b>.<br><br>"+
                     "Siz de bu projede çorbada tuzunuz bulunsun <b><i>isterseniz</i></b>, uygulamanın çalışmadığı veya beklenmedik tepkiler verdiği durumlarda sorunu geliştiriciye <i>bildirmeniz</i> ve <i>açıklamanız <b>bile</b></i> oldukça <i>faydalı olacaktır</i>. Geri bildirim göndermek için <i>\"Geri bildirim gönder\"</i> tuşuna basabilirsiniz. Eğer <i>yeterli teknik bilgiye</i> sahip olduğunuzu <i>düşünüyorsanız</i>, GitHub'da projenin kaynak kodlarında değişikliklerde, önerilerde ve iyileştirmelerde bulunabilirsiniz. <i>En küçük bir yardımınız</i> <b><i>dahi</i></b> projenin <i>sürdürülebilirliğine <u>müthiş</u></i> bir katkıda bulunacaktır.")