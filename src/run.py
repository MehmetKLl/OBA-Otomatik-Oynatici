from traceback import format_exc
from sys import exit
from requests import Session, exceptions
from utils.process import kill, start, process_list
from utils.env_paths import PROGRAM_PATH, TEMP_PATH, SETUP_PATH
from utils.log import Log
from runtools import registry, server, file, gui
from winreg import HKEY_CURRENT_USER

VERIFY_SSL = True

def start_installer():
    global VERIFY_SSL
    install_log = Log("Installer")
    
    install_log.write("Getting app contents from Github...")
    try:
        content_bytes = server.get_program_contents(timeout=3,verify=VERIFY_SSL)
    except exceptions.SSLError:
        install_log.write(f"An error occured due to SSL certificate authentication:\n{format_exc()}\n")
        
        ask_no_ssl_verify = gui.ask_and_show_error("SSL doğrulaması başarısız oldu. SSL doğrulamasını es geçip gene de devam etmek istiyor musunuz?\n(Bu yöntem güvenlik açıklarına sebep olacağından tavsiye edilmez.)","Player | Kurulum")        
        if ask_no_ssl_verify:
            VERIFY_SSL = False
            start_installer()
        else:
            exit(1)
            
    except exceptions.ConnectTimeout:
        install_log.write(f"Connection timed out:\n{format_exc()}\n")
        
        gui.show_error("Sunucuya gönderilen istek zaman aşımına uğradı.","Player | Kurulum")
        exit(1)
        
    except exceptions.ConnectionError:
        install_log.write(f"An error occured while getting app contents from Github:\n{format_exc()}\n")
        
        gui.show_error("Program internet olmadığından bilgisayara indirilemedi.","Player | Kurulum")
        exit(1)

    try:
        install_log.write(f"Creating temporary folder: \"{SETUP_PATH}\"")
        file.create_dir(SETUP_PATH)

        install_log.write(f"Downloading app contents...")
        file.write_byte(f"{SETUP_PATH}\\executable.zip",content_bytes)
        install_log.write(f"App contents have downloaded.")

        install_log.write(f"Creating contents' folder: \"{PROGRAM_PATH}\"")
        file.create_dir(PROGRAM_PATH)
        install_log.write(f"Contents' folder created: \"{PROGRAM_PATH}\"")

        install_log.write("Extracting contents from temporary zip file...")
        file.extract(f"{SETUP_PATH}\\executable.zip",PROGRAM_PATH)
        install_log.write("Contents have extracted from zip file.")

        install_log.write("Deleting temporary setup folder...")
        file.remove_all(SETUP_PATH)
        install_log.write("Temporary setup folder been deleted.")
            
        install_log.write("Creating registry value at: \"HKEY_CURRENT_USER\\SOFTWARE\\Player\\version\"")
        registry.create_key(HKEY_CURRENT_USER,"SOFTWARE\\Player","version",server.get_version())
        install_log.write("Created registry value at: \"HKEY_CURRENT_USER\\SOFTWARE\\Player\\version\"")

    except PermissionError as exc:
        install_log.write(f"An error occured due to system permissions:\n{format_exc()}\n")
        gui.show_error("Yetki hatası. Programı yönetici olarak çalıştırmayı deneyin.","Player | Kurulum")
        return 1

    except Exception as exc:
        exc_tb = format_exc()
        install_log.write(f"An unexpected error occured:\n{exc_tb}\n")
        gui.show_error(0,f"Beklenmedik bir hata oluştu:\n\n{exc_tb}", "Player | Kurulum")
        exit(1)

    else:
        install_log.write("Installation completed without any issues.")
        

def start_updater():
    global VERIFY_SSL
    updater_log = Log("Updater")
    
    updater_log.write("Getting version information from Github...")
    try:
        local_version = registry.read_key(HKEY_CURRENT_USER,"SOFTWARE\\Player","version")
        main_version = server.get_version()
    except exceptions.SSLError:
        updater_log.write(f"An error occured due to SSL certificate authentication:\n{format_exc()}\n")
        
        ask_no_ssl_verify = gui.ask_and_show_error("SSL doğrulaması başarısız oldu. SSL doğrumasını es geçip gene de devam etmek istiyor musunuz?\n(Bu yöntem güvenlik açıklarına sebep olacağından tavsiye edilmez.)","Player | Güncelleme Sistemi")        
        if ask_no_ssl_verify:
            VERIFY_SSL = False
            start_updater()
        else:
            pass
            
    except Exception:
        updater_log.write(f"An error occured while getting app contents from Github:\n{format_exc()}\n")
    
    else:
        if local_version == main_version:
            updater_log.write("Application is already up to date.")
        
        elif local_version != main_version:
            updater_log.write("Application isn't up to date.")

            updater_log.write("Getting app contents from Github...")
            try:
                content_bytes = server.get_program_contents(timeout=3,verify=VERIFY_SSL)
                
            except exceptions.ConnectTimeout:
                updater_log.write(f"Connection timed out:\n{format_exc()}\n")
            
                gui.show_error("Sunucuya gönderilen istek zaman aşımına uğradı.","Player | Kurulum")
                exit(1)
            
            except exceptions.ConnectionError:
                updater_log.write(f"An error occured while getting app contents from Github:\n{format_exc()}\n")
            
                gui.show_error("Program internet olmadığından bilgisayara indirilemedi.","Player | Kurulum")
                exit(1)
            
            
            try:
                if any(b"player_gui.exe.exe" in i for i in process_list()):
                    kill("player_gui.exe.exe")
                    updater_log.write("Killed 'player_gui.exe'")

                        
                updater_log.write(f"Creating temporary folder: \"{TEMP_PATH}\"")
                file.create_dir(TEMP_PATH)

                updater_log.write(f"Downloading app contents...")
                file.write_byte(f"{TEMP_PATH}\\executable.zip",content_bytes)
                updater_log.write(f"App contents have downloaded.")

                updater_log.write("App folder is cleaning...")
                file.remove_all(PROGRAM_PATH)
                file.create_dir(PROGRAM_PATH)
                updater_log.write("App folder been cleaned.")
                         
                updater_log.write("Extracting contents from temporary zip file...")
                file.extract(f"{TEMP_PATH}\\executable.zip",PROGRAM_PATH)
                updater_log.write("Contents have extracted from zip file.")

                updater_log.write("Deleting temporary folder...")
                file.remove_all(TEMP_PATH)
                updater_log.write("Temporary folder been deleted.")
                        
                updater_log.write("Updating registry value at: \"HKEY_CURRENT_USER\\SOFTWARE\\Player\\version\"")
                registry.create_key(HKEY_CURRENT_USER,"SOFTWARE\\Player","version",server.get_version())
                updater_log.write("Updated registry value at: \"HKEY_CURRENT_USER\\SOFTWARE\\Player\\version\"")

            except PermissionError as exc:
                gui.show_error("Yetki hatası. Uygulamayı yönetici olarak çalıştırmayı deneyin.", "Player | Güncelleme Sistemi")
                exit(1)

            except Exception as exc:
                exc_tb = format_exc()
                gui.show_error(f"Beklenmedik bir hata oluştu:\n\n{exc_tb}", "Player | Güncelleme Sistemi")
                exit(1)

            else:
                updater_log.write("Update completed without any issues.")
                        


def main():
    if not registry.check_key_exists(HKEY_CURRENT_USER,"SOFTWARE\\Player","version"):
        start_installer()
    else:
        start_updater()
    
    if not any(b"player_gui.exe" in i for i in process_list()):
        start(f"{PROGRAM_PATH}\\player_gui.exe")

    
    exit(0)

if __name__ == "__main__":
    main()
       
