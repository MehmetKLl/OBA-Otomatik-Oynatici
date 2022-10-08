from traceback import format_exc
from sys import exit
from requests import exceptions
from utils.process import start
from utils.env_paths import PROGRAM_PATH, TEMP_PATH, FULL_KEY_PATH, KEY_PATH, KEY_NAME
from utils.log import Log
from runtools import registry, server, file, gui
from winreg import HKEY_CURRENT_USER

verify_ssl = True
log = None  

def get_version_data():
    global verify_ssl
    
    log.write("Getting version information from Github...")
    try:
        return (0, server.get_version(verify=verify_ssl))
    except exceptions.SSLError:
        log.write(f"An error occured due to SSL certificate authentication:\n{format_exc()}\n")
        
        ask_no_ssl_verify = gui.ask_and_show_error("SSL doğrulaması başarısız oldu. SSL doğrumasını es geçip gene de devam etmek istiyor musunuz?\n(Bu yöntem güvenlik açıklarına sebep olacağından tavsiye edilmez.)","ÖBA Otomatik Oynatıcı | Güncelleme Sistemi")        
        if ask_no_ssl_verify:
            verify_ssl = False
            get_version_data()
        else:
            return (2, None)
            
    except Exception:
        log.write(f"An error occured while getting app contents from Github:\n{format_exc()}\n")
        return (2, None)
    

def set_registry_values(mode):
    global verify_ssl

    if mode not in ["update","install"]:
        raise ValueError(f"Mode must be \"update\" or \"install\", not \"{mode}\"")
    
    log.write(f"{'Updating' if mode == 'update' else 'Creating'} registry value at: \"{FULL_KEY_PATH}\"")
    try:
        registry.create_key(HKEY_CURRENT_USER,KEY_PATH,KEY_NAME,server.get_version(verify=verify_ssl))
    except exceptions.SSLError:
        log.write(f"An error occured due to SSL certificate authentication:\n{format_exc()}\n")
            
        ask_no_ssl_verify = gui.ask_and_show_error("Sürüm bilgisi alınırken SSL doğrulaması başarısız oldu. SSL doğrulamasını es geçip gene de devam etmek istiyor musunuz?\n(Bu yöntem güvenlik açıklarına sebep olacağından tavsiye edilmez.)",f"ÖBA Otomatik Oynatıcı | {'Kurulum' if mode == 'install' else 'Güncelleme Sistemi'}")        
        if ask_no_ssl_verify:
            verify_ssl = False
            return set_registry_values(mode)
                   
        else:
            return 1
                
    except exceptions.ConnectTimeout:
        log.write(f"Connection timed out:\n{format_exc()}\n")
                
        gui.show_error("Sürüm bilgisi alınırken sunucuya gönderilen istek zaman aşımına uğradı.",f"ÖBA Otomatik Oynatıcı | {'Kurulum' if mode == 'install' else 'Güncelleme Sistemi'}")
        return 1
            
    except exceptions.ConnectionError:
        log.write(f"An error occured while getting version information from Github:\n{format_exc()}\n")
                
        gui.show_error("Sürüm bilgisi internet mevcut olmadığından alınamadı.",f"ÖBA Otomatik Oynatıcı | {'Kurulum' if mode == 'install' else 'Güncelleme Sistemi'}")
        return 1
    else:
        log.write(f"{'Updated' if mode == 'update' else 'Created'} registry value at: \"{FULL_KEY_PATH}\"")

def install_program_contents(content_bytes,mode):
    if mode not in ["update","install"]:
        raise ValueError(f"Mode must be \"update\" or \"install\", not \"{mode}\"")
    
    try:
        log.write(f"Creating temporary folder: \"{TEMP_PATH}\"")
        file.create_dir(TEMP_PATH)

        log.write("Downloading app contents...")
        file.write_byte(f"{TEMP_PATH}\\executable.zip",content_bytes)
        log.write("App contents have downloaded.")

        if mode == "update":
            log.write("App folder is cleaning...")
            file.remove_all(PROGRAM_PATH)
            file.create_dir(PROGRAM_PATH)
            log.write("App folder been cleaned.")

        elif mode == "install":
            log.write(f"Creating app folder: \"{PROGRAM_PATH}\"")
            file.create_dir(PROGRAM_PATH)
            log.write(f"App folder created: \"{PROGRAM_PATH}\"")

        log.write("Extracting contents from temporary zip file...")
        file.extract(f"{TEMP_PATH}\\executable.zip",PROGRAM_PATH)
        log.write("Contents have extracted from zip file.")

        log.write("Deleting temporary setup folder...")
        file.remove_all(TEMP_PATH)
        log.write("Temporary setup folder been deleted.")
                
            
    except PermissionError as exc:
        gui.show_error("Yetki hatası. Uygulamayı yönetici olarak çalıştırmayı deneyin.", f"ÖBA Otomatik Oynatıcı | {'Kurulum' if mode == 'install' else 'Güncelleme Sistemi'}")
        return 1

    except Exception as exc:
        exc_tb = format_exc()
        gui.show_error(f"Beklenmedik bir hata oluştu:\n\n{exc_tb}", f"ÖBA Otomatik Oynatıcı | {'Kurulum' if mode == 'install' else 'Güncelleme Sistemi'}")
        return 1

    else:
        return 0

def download_program_contents(mode):
    global verify_ssl

    if mode not in ["update","install"]:
        raise ValueError(f"Mode must be \"update\" or \"install\", not \"{mode}\"")
    
    log.write("Getting app contents from Github...")
    try:
        return (0, server.get_program_contents(timeout=3,verify=verify_ssl))
    except exceptions.SSLError:
        log.write(f"An error occured due to SSL certificate authentication:\n{format_exc()}\n")
        
        ask_no_ssl_verify = gui.ask_and_show_error("SSL doğrulaması başarısız oldu. SSL doğrulamasını es geçip gene de devam etmek istiyor musunuz?\n(Bu yöntem güvenlik açıklarına sebep olacağından tavsiye edilmez.)",f"ÖBA Otomatik Oynatıcı | {'Kurulum' if mode == 'install' else 'Güncelleme Sistemi'}")        
        if ask_no_ssl_verify:
           verify_ssl = False
           return download_program_contents(mode)
               
        else:
            return (1, None)
            
    except exceptions.ConnectTimeout:
        log.write(f"Connection timed out:\n{format_exc()}\n")
            
        gui.show_error("Sunucuya gönderilen istek zaman aşımına uğradı.",f"ÖBA Otomatik Oynatıcı | {'Kurulum' if mode == 'install' else 'Güncelleme Sistemi'}")
        return (1, None)
        
    except exceptions.ConnectionError:
        log.write(f"An error occured while getting app contents from Github:\n{format_exc()}\n")
            
        gui.show_error("Program internet olmadığından bilgisayara indirilemedi.",f"ÖBA Otomatik Oynatıcı | {'Kurulum' if mode == 'install' else 'Güncelleme Sistemi'}")
        return (1, None)
        

def start_installer():
    return_code, content_bytes = download_program_contents(mode="install")
    if return_code:
        log.close()
        exit(1)


    return_code = install_program_contents(content_bytes,mode="install")
    if return_code:
        log.close()
        exit(1)

    return_code = set_registry_values(mode="install")
    if return_code:
        log.close()
        exit(1)

    log.write("Installation completed without any issues.")
    log.close()

    
def start_updater():
    log.write(f"Reading registry value at: \"{FULL_KEY_PATH}\"")
    local_version = registry.read_key(HKEY_CURRENT_USER,KEY_PATH,KEY_NAME)
    log.write(f"Read registry value at: \"{FULL_KEY_PATH}\"")

    
    return_code, main_version = get_version_data()

    if return_code:
        log.close()
        return
    
    
    if local_version == main_version:
        log.write("Application is already up to date.")
        
    elif local_version != main_version:
        log.write("Application isn't up to date.")
            
        return_code, content_bytes = download_program_contents(mode="update")
        if return_code:
            log.close()
            exit(1)

         
        return_code = install_program_contents(content_bytes,mode="update")
        if return_code:
            log.close()
            exit(1)


        return_code = set_registry_values(mode="update")
        if return_code:
            log.close()
            exit(1)

        log.write("Update completed without any issues.")
        log.close()



def main():
    global log
    
    if not registry.check_key_exists(HKEY_CURRENT_USER,KEY_PATH,KEY_NAME):
        log = Log("Installer")
        start_installer()
    else:
        log = Log("Updater")
        start_updater()
    
    start(f"{PROGRAM_PATH}\\oba_gui.exe")

    log.close()
    exit(0)

if __name__ == "__main__":
    main()
        

    
    
