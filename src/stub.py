from utils.constants import File, Registry, InstallerDialogs
from utils.process import run_cmd, process_list
from winreg import HKEY_CURRENT_USER
from traceback import format_exc
from requests import exceptions
from os import rename, path
import errno as error_codes
from sys import argv, exit
from time import sleep
import utils.registry
import utils.dialogs
import utils.github
import utils.file
import utils.log

dialog_title = InstallerDialogs.STUB_TITLE

def download_bootstrapper_contents(version = "latest", verify = True):
    utils.log.log.write("Getting new bootstrapper contents from Github...")

    try:
        return (0, utils.github.get_bootstrapper_contents(version, timeout = 3, verify = verify))
    
    except exceptions.SSLError:
        utils.log.log.write(f"An error occured due to SSL certificate authentication:\n{format_exc()}\n")

        ask_no_ssl_verify = utils.dialogs.ask_warning("Yükleyici indirilirken SSL doğrulaması başarısız oldu. SSL doğrulamasını es geçip yine de devam etmek istiyor musunuz?\n\nBu durum kurumsal ağlarda ağ güvenlik politikaları doğrultusunda yapılan uygulamalardan dolayı beklenen bir durumdur. *Ancak*, SSL doğrulamanın kapatılması sonucunda ağ yöneticisi ya da internet sağlayıcısı uygulamanın ağ trafiğini izleyebilir, ya da kötü amaçlı kişiler tarafından sunucudan gelen içerik daha bilgisayarınıza gelmeden değiştirilip zararlı yazılımlar yüklenmesine sebep olabilir. Bu sebeplerden ötürü doğrulamayı kapatmak halka açık ortak ağlarda kesinlikle tavsiye edilmez.", dialog_title)        
        if ask_no_ssl_verify:
           return download_bootstrapper_contents(version, False)

        else:
            return (1, None)

    except (exceptions.ConnectTimeout, exceptions.ReadTimeout):
        utils.log.log.write(f"Connection timed out:\n{format_exc()}\n")

        utils.dialogs.show_error("Yükleyiciyi indirmek için sunucuya gönderilen istek zaman aşımına uğradı.", dialog_title)
        return (1, None)

    except exceptions.ConnectionError:
        utils.log.log.write(f"An error occured while getting bootstrapper contents from Github:\n{format_exc()}\n")

        utils.dialogs.show_error("Yeni yükleyici internet olmadığından bilgisayara indirilemedi.", dialog_title)
        return (1, None)

def install_bootstrapper_contents(content_bytes):
    try:
        utils.log.log.write("Downloading bootstrapper contents...")
        utils.file.write_byte(f"{File.STUB_PATH}\\bootstrapper.zip", content_bytes)
        utils.log.log.write("Bootstrapper contents have been downloaded.")

        utils.log.log.write("Extracting contents from temporary zip file...")
        utils.file.extract(f"{File.STUB_PATH}\\bootstrapper.zip", File.STUB_PATH)
        utils.log.log.write("Contents have been extracted from zip file.")

    except OSError as exc:
        error_code = exc.errno
        exc_tb = format_exc()

        utils.log.log.write(f"An OS related error occured while installing bootstrapper contents:\n{exc_tb}")

        if error_code == error_codes.ENOENT:
            utils.dialogs.show_error("Yeni yükleyici kurulurken aranılan dosya ya da dizin bulunamadı.", dialog_title)

        elif error_code == error_codes.ENOSPC:
            utils.dialogs.show_error("Yeni yükleyici kurulurken bilgisayarda boş yer kalmadı. Birkaç gereksiz dosyayı silmeyi deneyin.", dialog_title)

        elif error_code == error_codes.ENOMEM:
            utils.dialogs.show_error("Yeni yükleyici kurulurken bir hata oluştu: Uygulamanın kullanabileceği bellek miktarı yetersiz.", dialog_title)

        elif error_code in (error_codes.EPERM, error_codes.EACCES):
            utils.dialogs.show_error("Yeni yükleyici kurulurken bir yetki hatası oluştu. Programı yönetici olarak çalıştırmayı deneyin.", dialog_title)

        else:
            utils.dialogs.show_error(f"Yeni yükleyici kurulduğu esnada çözümlenemeyen bir sebepten işletim sistemi hatası oluştu:\n\n{exc_tb}", dialog_title)

        return 1

    except Exception as exc:
        exc_tb = format_exc()
        utils.log.log.write(f"An unexpected error occured while installing new bootstrapper contents:\n{exc_tb}")
        utils.dialogs.show_error(f"Yeni yükleyici kurulurken beklenmedik bir hata oluştu:\n\n{exc_tb}", dialog_title)
        return 1

    return 0


def check_is_app_running():
    try:
        return (0, "oba_gui.exe" in process_list())

    except OSError as exc:
        error_code = exc.errno
        exc_tb = format_exc()

        utils.log.log.write(f"An OS related error occured while fetching process list:\n{exc_tb}")

        if error_code in (error_codes.EPERM, error_codes.EACCES):
            utils.dialogs.show_error("Çalışan işlemler kontrol edilirken yetki hatası oluştu. Programı yönetici olarak çalıştırmayı deneyin.", dialog_title)

        else:
            utils.dialogs.show_error(f"Çalışan işlemler kontrol edilirken çözümlenemeyen bir sebepten işletim sistemi hatası oluştu:\n\n{exc_tb}", dialog_title)

        return (1, None)

    except Exception as exc:
        exc_tb = format_exc()
        utils.log.log.write(f"An unexpected error occured while fetching process list:\n{exc_tb}")
        utils.dialogs.show_error(f"Çalışan işlemler kontrol edilirken beklenmedik bir hata oluştu:\n\n{exc_tb}", dialog_title)
        return (1, None)

def clone_and_rename_stub():
    try:
        if path.exists(File.STUB_PATH):
            utils.log.log.write("Stub folder is cleaning...")
            utils.file.remove_in(File.STUB_PATH)
            utils.log.log.write("Stub folder has been cleaned.")

        else:
            utils.log.log.write(f"Creating temporary stub folder: \"{File.STUB_PATH}\"")
            utils.file.create_folder(File.STUB_PATH)

        utils.file.copy_directory(File.PROGRAM_PATH, File.STUB_PATH)
        rename(f"{File.STUB_PATH}\\oba_gui.exe", f"{File.STUB_PATH}\\oba_ot_stub.exe")

    except OSError as exc:
        error_code = exc.errno
        exc_tb = format_exc()

        utils.log.log.write(f"An OS related error occured while moving stub to a new directory:\n{exc_tb}")

        if error_code == error_codes.ENOENT:
            utils.dialogs.show_error("Uyumluluk yöneticisi başka bir dizine taşınırken aranılan dosya ya da dizin bulunamadı.", dialog_title)

        elif error_code == error_codes.ENOSPC:
            utils.dialogs.show_error("Uyumluluk yöneticisi başka bir yere taşınırken bilgisayarda boş yer kalmadı. Birkaç gereksiz dosyayı silmeyi deneyin.", dialog_title)

        elif error_code == error_codes.ENOMEM:
            utils.dialogs.show_error("Uyumluluk yöneticisi taşınırken bir hata oluştu: Uygulamanın kullanabileceği bellek miktarı yetersiz.", dialog_title)

        elif error_code in (error_codes.EPERM, error_codes.EACCES):
            utils.dialogs.show_error("Uyumluluk yöneticisi başka bir dizine taşınırken yetki hatası oluştu. Programı yönetici olarak çalıştırmayı deneyin.", dialog_title)

        else:
            utils.dialogs.show_error(f"Uyumluluk yöneticisi başka bir dizine taşınırken çözümlenemeyen bir sebepten işletim sistemi hatası oluştu:\n\n{exc_tb}", dialog_title)

        return 1

    except Exception as exc:
        exc_tb = format_exc()
        utils.log.log.write(f"An unexpected error occured while moving stub to a new directory:\n{exc_tb}")
        utils.dialogs.show_error(f"Uyumluluk yöneticisi başka bir dizine taşınırken beklenmedik bir hata oluştu:\n\n{exc_tb}", dialog_title)
        return 1
    
    return 0

def wait_until_app_terminated():
    while True:
        is_error_occured, is_app_running = check_is_app_running()

        if is_error_occured:
            return 1

        if not is_app_running:
            return 0

        sleep(0.25)

def prepare_for_installation_mode():
    try:
        utils.log.log.write(f"Deleting registry value at: \"{Registry.VERSION_FULL_KEY_PATH}\" to trigger bootstrapper's installation mode...")
        utils.registry.delete_key(HKEY_CURRENT_USER, Registry.KEY_PATH, Registry.VERSION_KEY_NAME)
        utils.log.log.write(f"Deleted registry value at: \"{Registry.VERSION_FULL_KEY_PATH}\".")

    except OSError as exc:
        error_code = exc.errno
        exc_tb = format_exc()

        utils.log.log.write(f"An OS related error occured while deleting version registry key:\n{exc_tb}")

        if error_code == error_codes.ENOENT:
            utils.dialogs.show_error("Aranılan dosya ya da dizin bulunamadı.", dialog_title)

        elif error_code in (error_codes.EPERM, error_codes.EACCES):
            utils.dialogs.show_error("Yetki hatası oluştu. Programı yönetici olarak çalıştırmayı deneyin.", dialog_title)

        else:
            utils.dialogs.show_error(f"Çözümlenemeyen bir sebepten işletim sistemi hatası oluştu:\n\n{exc_tb}", dialog_title)

        return 1
    
    except Exception as exc:
        exc_tb = format_exc()
        utils.log.log.write(f"An unexpected error occured while deleting version registry key:\n{exc_tb}")
        utils.dialogs.show_error(f"Kayıt defteri değerleri oluşturulup yazılırken beklenmedik bir hata oluştu:\n\n{exc_tb}", dialog_title)
        return 1
    
    return 0

def start_first_run():
    is_error_occured = clone_and_rename_stub()
    if is_error_occured:
        utils.log.log.close()
        exit(1)

    utils.log.log.write("Starting to install new bootstrapper...")

    is_error_occured, content_bytes = download_bootstrapper_contents()
    if is_error_occured:
        utils.log.log.close()
        exit(1)

    is_error_occured = install_bootstrapper_contents(content_bytes)
    if is_error_occured:
        utils.log.log.close()
        exit(1)

    utils.log.log.write("Bootstrapper installation completed without any issues.")

    utils.log.log.write("Executing relocated stub file and aborting...")
    utils.log.log.close()

    run_cmd([f"{File.STUB_PATH}\\oba_ot_stub.exe", "--relocated"])

    exit(0)

def start_relocated_run():
    is_error_occured = wait_until_app_terminated()
    if is_error_occured:
        utils.log.log.close()
        exit(1)

    is_error_occured = prepare_for_installation_mode()
    if is_error_occured:
        utils.log.log.close()
        exit(1)

    utils.dialogs.show_warning("\"oba_otomatik_oynatma.exe\" dosyasının eski bir sürümünü kullanıyorsunuz.\n\nÇalıştırdığınız mevcut dosya güncellemeyi doğru şekilde alabilmek için yeni \"oba_otomatik_oynatma.exe\" dosyasını indirdi. Bu mesaj kutusu kapatıldıktan sonra bu yeni dosya çalıştırılacak.\n\nGelecekte ilerleyen sürümlerle beraber eski güncelleme sisteminin tamamen devre dışı bırakılması düşünülmekte. Bu durum gerçekleştiği zaman eski sürüm dosyaların maalesef işlevselliği kaybolacak. Dolayısıyla, uygulamayı açarken sorun yaşamamanız için yeni \"oba_otomatik_oynatma.exe\" dosyasını GitHub sayfasından indirmenizi kuvvetle öneriyoruz.", dialog_title)

    utils.log.log.write("Executing new bootstrapper...")
    bootstrapper_process = run_cmd([f"{File.STUB_PATH}\\oba_otomatik_oynatma.exe"])
    return_bytes, return_code = bootstrapper_process.communicate(), bootstrapper_process.returncode

    if return_bytes[1] or return_code:
        utils.log.log.write(f"An error occured in executed new bootstrapper and process is terminated:\n{return_bytes[1]}")
        utils.log.log.close()
        utils.dialogs.show_error("Yeni oba_otomatik_oynatma.exe dosyası çalıştırılırken beklenmedik bir hata oluştu ve program sonlandırıldı.", dialog_title)
        exit(1)
    
    utils.log.log.close()
    exit(0)

def main():
    utils.log.create_log("log", "Stub")

    if "--relocated" in argv:
        start_relocated_run()
    
    else:
        start_first_run()

if __name__ == "__main__":
    main()