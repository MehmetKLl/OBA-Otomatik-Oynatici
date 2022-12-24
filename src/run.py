from winreg import HKEY_CURRENT_USER
from traceback import format_exc
from sys import exit
from requests import exceptions
from utils.process import kill, start
from utils.constants import File, Registry, InstallerDialogs
import utils.log
import utils.github
import utils.dialogs
import utils.registry
import utils.file
import errno as error_codes

verify_ssl = True 

def get_version_data():
    global verify_ssl

    utils.log.log.write("Getting version information from Github...")
    try:
        return (0, utils.github.get_version(verify=verify_ssl))
    except exceptions.SSLError:
        utils.log.log.write(f"An error occured due to SSL certificate authentication:\n{format_exc()}\n")
        
        ask_no_ssl_verify = utils.dialogs.ask_error("SSL doğrulaması başarısız oldu. SSL doğrumasını es geçip gene de devam etmek istiyor musunuz?\n(Bu yöntem güvenlik açıklarına sebep olacağından tavsiye edilmez.)",InstallerDialogs.UPDATER_TITLE)        
        if ask_no_ssl_verify:
            verify_ssl = False
            get_version_data()
        
        return (2, None)
            
    except Exception:
        utils.log.log.write(f"An error occured while getting app contents from Github:\n{format_exc()}\n")
        return (2, None)


def set_registry_values(mode):
    global verify_ssl

    if mode not in ["update","install"]:
        raise ValueError(f"Mode must be \"update\" or \"install\", not \"{mode}\"")

    if mode == "update":
        dialog_title = InstallerDialogs.UPDATER_TITLE
    
    elif mode == "install":
        dialog_title = InstallerDialogs.INSTALLER_TITLE

    utils.log.log.write(f"Creating \"{Registry.LASTCRASH_KEY_NAME}\" registry key at: \"{Registry.LASTCRASH_FULL_KEY_PATH}\"")
    
    utils.log.log.write(f"{'Updating' if mode == 'update' else 'Creating'} registry value at: \"{Registry.VERSION_FULL_KEY_PATH}\"")
    try:
        utils.registry.create_key(HKEY_CURRENT_USER,Registry.KEY_PATH,Registry.VERSION_KEY_NAME,utils.github.get_version(verify=verify_ssl))
        utils.registry.create_key(HKEY_CURRENT_USER,Registry.KEY_PATH,Registry.LASTCRASH_KEY_NAME,"-1")

    except exceptions.SSLError:
        utils.log.log.write(f"An error occured due to SSL certificate authentication:\n{format_exc()}\n")
            
        ask_no_ssl_verify = utils.dialogs.ask_error(f"Sürüm bilgisi alınırken SSL doğrulaması başarısız oldu. SSL doğrulamasını es geçip gene de devam etmek istiyor musunuz?\n(Bu yöntem güvenlik açıklarına sebep olacağından tavsiye edilmez.)",InstallerDialogs.INSTALLER_TITLE if mode == 'install' else InstallerDialogs.UPDATER_TITLE)        
        if ask_no_ssl_verify:
            verify_ssl = False
            return set_registry_values(mode)
                   
        return 1
                
    except exceptions.ConnectTimeout:
        utils.log.log.write(f"Connection timed out:\n{format_exc()}\n")
                
        utils.dialogs.show_error(f"Sürüm bilgisi alınırken sunucuya gönderilen istek zaman aşımına uğradı.", dialog_title)
        return 1
            
    except exceptions.ConnectionError:
        utils.log.log.write(f"An error occured while getting version information from Github:\n{format_exc()}\n")
                
        utils.dialogs.show_error(f"Sürüm bilgisi internet mevcut olmadığından alınamadı.", dialog_title)
        return 1
    
    except OSError as exc:
        error_code = exc.__class__.errno

        if error_code == error_codes.ENOENT:
            utils.dialogs.show_error("Aranılan dosya ya da dizin bulunamadı.", dialog_title)

        elif error_code in (error_codes.EPERM, error_codes.EACCES):
            utils.dialogs.show_error("Yetki hatası oluştu. Programı yönetici olarak çalıştırmayı deneyin.", dialog_title)

        else:
            exc_tb = format_exc()
            utils.dialogs.show_error(f"Çözümlenemeyen bir sebepten işletim sistemi hatası oluştu:\n\n{exc_tb}", dialog_title)

        return 1
    
    utils.log.log.write(f"{'Updated' if mode == 'update' else 'Created'} registry value at: \"{Registry.VERSION_FULL_KEY_PATH}\"")
    utils.log.log.write(f"Created \"{Registry.LASTCRASH_KEY_NAME}\" registry key at: \"{Registry.LASTCRASH_FULL_KEY_PATH}\"")

def check_key_exists():
    dialog_title = InstallerDialogs.TITLE

    try:
        return utils.registry.check_key_exists(HKEY_CURRENT_USER,Registry.KEY_PATH,Registry.VERSION_KEY_NAME)
    
    except OSError as exc:
        error_code = exc.errno

        if error_code in (error_codes.EPERM, error_codes.EACCES):
            utils.dialogs.show_error("Kayıt defteri değeri okunurken yetki hatası oluştu. Programı yönetici olarak çalıştırmayı deneyin.", dialog_title)

        else:
            exc_tb = format_exc()
            utils.dialogs.show_error(f"Kayıt defteri değeri okunurken çözümlenemeyen bir sebepten işletim sistemi hatası oluştu:\n\n{exc_tb}", dialog_title)
        
        exit(1)

    except Exception as exc:
        exc_tb = format_exc()
        utils.dialogs.show_error(f"Kayıt defteri değeri okunurken beklenmedik bir hata oluştu:\n\n{exc_tb}", dialog_title)
        exit(1)


def install_program_contents(content_bytes,mode):
    global verify_ssl

    if mode not in ["update","install"]:
        raise ValueError(f"Mode must be \"update\" or \"install\", not \"{mode}\"")
    
    if mode == "update":
        dialog_title = InstallerDialogs.UPDATER_TITLE
    
    elif mode == "install":
        dialog_title = InstallerDialogs.INSTALLER_TITLE
    
    try:
        utils.log.log.write(f"Creating temporary folder: \"{File.TEMP_PATH}\"")
        utils.file.create_folder(File.TEMP_PATH)

        utils.log.log.write(f"Downloading app contents...")
        utils.file.write_byte(f"{File.TEMP_PATH}\\executable.zip",content_bytes)
        utils.log.log.write(f"App contents have downloaded.")

        if mode == "update":
            utils.log.log.write("App folder is cleaning...")
            utils.file.remove_in(File.PROGRAM_PATH)
            utils.log.log.write("App folder been cleaned.")

        elif mode == "install":
            utils.log.log.write(f"Creating app folder: \"{File.PROGRAM_PATH}\"")
            utils.file.create_folder(File.PROGRAM_PATH)
            utils.log.log.write(f"App folder created: \"{File.PROGRAM_PATH}\"")

        utils.log.log.write("Extracting contents from temporary zip file...")
        utils.file.extract(f"{File.TEMP_PATH}\\executable.zip",File.PROGRAM_PATH)
        utils.log.log.write("Contents have extracted from zip file.")

        utils.log.log.write("Deleting temporary setup folder...")
        utils.file.remove_all(File.TEMP_PATH)
        utils.log.log.write("Temporary setup folder been deleted.")
                          
    except OSError as exc:
        error_code = exc.__class__.errno

        if error_code == error_codes.ENOENT:
            utils.dialogs.show_error("Aranılan dosya ya da dizin bulunamadı.", dialog_title)
        
        elif error_code == error_codes.ENOSPC:
            utils.dialogs.show_error("Bilgisayarda boş yer kalmadı. Birkaç gereksiz dosyayı silmeyi deneyin.", dialog_title)

        elif error_code == error_codes.ENOMEM:
            utils.dialogs.show_error("Uygulamanın kullanabileceği bellek miktarı yetersiz.", dialog_title)

        elif error_code in (error_codes.EPERM, error_codes.EACCES):
            utils.dialogs.show_error("Yetki hatası oluştu. Programı yönetici olarak çalıştırmayı deneyin.", dialog_title)
        
        else:
            exc_tb = format_exc()
            utils.dialogs.show_error(f"Çözümlenemeyen bir sebepten işletim sistemi hatası oluştu:\n\n{exc_tb}", dialog_title)

        return 1

    except Exception as exc:
        exc_tb = format_exc()
        utils.dialogs.show_error(f"Beklenmedik bir hata oluştu:\n\n{exc_tb}", dialog_title)
        return 1
   
    return 0


def download_program_contents(mode):
    global verify_ssl

    if mode not in ["update","install"]:
        raise ValueError(f"Mode must be \"update\" or \"install\", not \"{mode}\"")
    
    utils.log.log.write("Getting app contents from Github...")
    try:
        return (0, utils.github.get_program_contents(timeout=3,verify=verify_ssl))
    except exceptions.SSLError:
        utils.log.log.write(f"An error occured due to SSL certificate authentication:\n{format_exc()}\n")
        
        ask_no_ssl_verify = utils.dialogs.ask_error(f"SSL doğrulaması başarısız oldu. SSL doğrulamasını es geçip gene de devam etmek istiyor musunuz?\n(Bu yöntem güvenlik açıklarına sebep olacağından tavsiye edilmez.)",InstallerDialogs.INSTALLER_TITLE if mode == 'install' else InstallerDialogs.UPDATER_TITLE)        
        if ask_no_ssl_verify:
           verify_ssl = False
           return download_program_contents(mode)
               
        else:
            return (1, None)
            
    except exceptions.ConnectTimeout:
        utils.log.log.write(f"Connection timed out:\n{format_exc()}\n")
            
        utils.dialogs.show_error(f"Sunucuya gönderilen istek zaman aşımına uğradı.",InstallerDialogs.INSTALLER_TITLE if mode == 'install' else InstallerDialogs.UPDATER_TITLE)
        return (1, None)
        
    except exceptions.ConnectionError:
        utils.log.log.write(f"An error occured while getting app contents from Github:\n{format_exc()}\n")
            
        utils.dialogs.show_error(f"Program internet olmadığından bilgisayara indirilemedi.",InstallerDialogs.INSTALLER_TITLE if mode == 'install' else InstallerDialogs.UPDATER_TITLE)
        return (1, None)
        

def start_installer():
    is_error_occured, content_bytes = download_program_contents(mode="install")
    if is_error_occured:
        utils.log.log.close()
        exit(1)

    if install_program_contents(content_bytes,mode="install"):
        utils.log.log.close()
        exit(1)

    if set_registry_values(mode="install"):
        utils.log.log.close()
        exit(1)

    utils.log.log.write("Installation completed without any issues.")
    utils.log.log.close()

    
def start_updater():
    utils.log.log.write(f"Reading registry value at: \"{Registry.VERSION_FULL_KEY_PATH}\"")
    local_version = utils.registry.read_key(HKEY_CURRENT_USER,Registry.KEY_PATH,Registry.VERSION_KEY_NAME)
    utils.log.log.write(f"Read registry value at: \"{Registry.VERSION_FULL_KEY_PATH}\"")

    is_error_occured, main_version = get_version_data()

    if is_error_occured:
        utils.log.log.close()
        return
    
    if local_version == main_version:
        utils.log.log.write("Application is already up to date.")
        
    elif local_version != main_version:
        utils.log.log.write("Application isn't up to date.")

        ask_for_update = utils.dialogs.ask_info(f"Programın yeni bir sürümü mevcut. Programı yeni sürüme güncellemek ister misiniz?\n\nBilgisayarda yüklü olan sürüm: {local_version}\nSon sürüm: {main_version}",InstallerDialogs.UPDATER_TITLE)
        if not ask_for_update:
            utils.log.log.close()
            return
            
        is_error_occured, content_bytes = download_program_contents(mode="update")
        if is_error_occured:
            utils.log.log.close()
            exit(1)
         
        if install_program_contents(content_bytes,mode="update"):
            utils.log.log.close()
            exit(1)

        if set_registry_values(mode="update"):
            utils.log.log.close()
            exit(1)

        utils.log.log.write("Update completed without any issues.")
        utils.log.log.close()


def start_troubleshooter():
    start_repair = utils.dialogs.ask_error("Hali hazırda yüklü olan programda hata oluştu ve program başlatılamadı/çöktü. Otomatik tamir işlemini başlatmak istiyor musunuz?", InstallerDialogs.TROUBLESHOOTER_TITLE)
    
    if not start_repair:
        return

    utils.log.log.write("Starting auto-repair process...")
    
    is_error_occured, content_bytes = download_program_contents(mode="install")
    if is_error_occured:
        utils.log.log.close()
        utils.dialogs.show_error("Otomatik tamir işlemi başarısız oldu. Programı yeniden çalıştırmayı deneyin.", InstallerDialogs.TROUBLESHOOTER_TITLE)
        exit(1)

    if install_program_contents(content_bytes,mode="install"):
        utils.log.log.close()
        utils.dialogs.show_error("Otomatik tamir işlemi başarısız oldu. Programı yeniden çalıştırmayı deneyin.", InstallerDialogs.TROUBLESHOOTER_TITLE)
        exit(1)

    if set_registry_values(mode="install"):
        utils.log.log.close()
        utils.dialogs.show_error("Otomatik tamir işlemi başarısız oldu. Programı yeniden çalıştırmayı deneyin.", InstallerDialogs.TROUBLESHOOTER_TITLE)
        exit(1)

    utils.log.log.write("Auto-repair process completed without any issues.")
    utils.log.log.close()


def main():
    kill("oba_gui.exe")

    if not check_key_exists():
        utils.log.create_log("log","Installer")
        start_installer()
    else:
        utils.log.create_log("log","Updater")
        start_updater()
    
    utils.log.log.close()
    
    gui_process = start(f"{File.PROGRAM_PATH}\\oba_gui.exe")

    return_bytes, return_code = gui_process.communicate(), gui_process.returncode
    
    if return_bytes[1] or return_code:
        if utils.registry.read_key(HKEY_CURRENT_USER,Registry.KEY_PATH,Registry.LASTCRASH_KEY_NAME) == "1":
            utils.log.create_log("log","Troubleshooter")
            start_troubleshooter()

            start(f"{File.PROGRAM_PATH}\\oba_gui.exe")
            utils.log.log.close()
            exit(0)

        utils.registry.create_key(HKEY_CURRENT_USER,Registry.KEY_PATH,Registry.LASTCRASH_KEY_NAME,"1")
        exit(1)
    

    utils.registry.create_key(HKEY_CURRENT_USER,Registry.KEY_PATH,Registry.LASTCRASH_KEY_NAME,"0")
    utils.log.log.close()
    exit(0)


if __name__ == "__main__":
    main()