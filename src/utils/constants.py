from os import environ

VERSION = "1.4.6"

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
    #LICENSE_TEXT =  ("Telif Hakkı (c) 2022 ÖBA Otomatik Oynatıcı\n\n" +
    #                 "Hiçbir ücret talep edilmeden burada işbu yazılımın bir kopyasını ve belgelendirme dosyalarını (“Yazılım”) elde eden herkese verilen izin; kullanma, kopyalama, değiştirme, birleştirme, yayımlama, dağıtma, alt lisanslama, ve/veya yazılımın kopyalarını satma eylemleri de dahil olmak üzere ve bununla kısıtlama olmaksızın, yazılımın sınırlama olmadan ticaretini yapmak için verilmiş olup, bunları yapmaları için yazılımın sağlandığı kişilere aşağıdakileri yapmak koşuluyla sunulur:\n\n" +
    #                 "Yukarıdaki telif hakkı bildirimi ve işbu izin bildirimi yazılımın tüm kopyalarına veya önemli parçalarına eklenmelidir.\n\n" +
    #                 "YAZILIM “HİÇBİR DEĞİŞİKLİK YAPILMADAN” ESASINA BAĞLI OLARAK, TİCARETE ELVERİŞLİLİK, ÖZEL BİR AMACA UYGUNLUK VE İHLAL OLMAMASI DA DAHİL VE BUNUNLA KISITLI OLMAKSIZIN AÇIKÇA VEYA ÜSTÜ KAPALI OLARAK HİÇBİR TEMİNAT OLMAKSIZIN SUNULMUŞTUR. HİÇBİR KOŞULDA YAZARLAR VEYA TELİF HAKKI SAHİPLERİ HERHANGİ BİR İDDİAYA, HASARA VEYA DİĞER YÜKÜMLÜLÜKLERE KARŞI, YAZILIMLA VEYA KULLANIMLA VEYA YAZILIMIN BAŞKA BAĞLANTILARIYLA İLGİLİ, BUNLARDAN KAYNAKLANAN VE BUNLARIN SONUCU BİR SÖZLEŞME DAVASI, HAKSIZ FİİL VEYA DİĞER EYLEMLERDEN SORUMLU DEĞİLDİR.")


class Player:
    SCROLL_DELAY = 1
    VIDEO_CHECK_DELAY = 5
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

