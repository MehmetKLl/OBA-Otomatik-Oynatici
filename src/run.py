from traceback import format_exc
from sys import exit
from utils.process import kill, start, process_list
from utils.env_paths import *
from utils.log import Log
from runtools.registry import *
from runtools.server import *
from runtools.file import *
from winreg import HKEY_CURRENT_USER
from win32api import MessageBox
from win32con import MB_OK, MB_YESNO, MB_ICONERROR

if __name__ == "__main__":
    
    VERIFICATE_SSL = True
    
    if not check_key(HKEY_CURRENT_USER,"SOFTWARE\\OBA Otomatik Oynatici","version"):
        
        install_log = Log("Installer")
        install_log.write("Getting app contents from Github...")
        try:
            content_bytes = get_program_contents(timeout=3,verify=VERIFICATE_SSL)
        except Exception as exc:
            exc_type = exc.__class__.__name__.lower()
            install_log.write(f"An error occured while getting app contents from Github:\n{format_exc()}\n")
            
            if exc_type == "connectionerror":
                MessageBox(0,"İnternet bağlantısı mevcut olmadığından program karşıdan yüklenemedi.", "ÖBA Otomatik Oynatıcı | Kurulum", MB_OK | MB_ICONERROR)
                exit(1)
                
            elif exc_type == "connecttimeout":
                MessageBox(0,"İnternet bağlantınız yavaş olduğundan sunucu ile iletişim zaman aşımına uğradı.", "ÖBA Otomatik Oynatıcı | Kurulum", MB_OK | MB_ICONERROR)
                exit(1)
                
            elif exc_type == "sslerror":
                req_without_verify = MessageBox(0,"Sunucu ile SSL sertifikası doğrulaması başarısız oldu. SSL sertifika doğrulamasını pas geçip gene de devam etmek istiyor musunuz?\n\n(Bu durum güvenlik açıklarına sebep olabileceğinden tavsiye edilmez.)", "ÖBA Otomatik Oynatıcı | Kurulum", MB_YESNO | MB_ICONERROR)

                if req_without_verify == 6:
                    VERIFICATE_SSL = False
                    install_log.write("Attempting again to get version information from Github...")
                    try:
                        content_bytes = get_program_contents(timeout=3, verify=VERIFICATE_SSL)
                    except Exception as exc:
                        install_log.write(f"Attempt failed:\n{format_exc()}\n")
                        MessageBox(0,"Sunucu ile bağlantı kurulurken hata oluştu. Programı kişisel ağ üzerinde kurmayı deneyin.", "ÖBA Otomatik Oynatıcı | Kurulum", MB_OK | MB_ICONERROR)    
                        exit(1)
                else:
                    exit(1)
            
        try:
            install_log.write(f"Creating temporary folder: \"{SETUP_PATH}\"")
            create_dir(SETUP_PATH)

            install_log.write("Downloading app contents...")
            write_byte(f"{SETUP_PATH}\\executable.zip","wb",content_bytes)
            install_log.write("App contents have downloaded.")

            install_log.write(f"Creating contents' folder: \"{PROGRAM_PATH}\"")
            create_dir(PROGRAM_PATH)
            install_log.write(f"Contents' folder created: \"{PROGRAM_PATH}\"")

            install_log.write("Extracting contents from temporary zip file...")
            extract(f"{SETUP_PATH}\\executable.zip",PROGRAM_PATH)
            install_log.write("Contents have extracted from zip file.")

            install_log.write("Deleting temporary setup folder...")
            removeall(SETUP_PATH)
            install_log.write("Temporary setup folder been deleted.")
            
            install_log.write("Creating registry value at: \"HKEY_CURRENT_USER\\SOFTWARE\\OBA Otomatik Oynatici\\version\"")
            create_key(HKEY_CURRENT_USER,"SOFTWARE\\OBA Otomatik Oynatici","version",get_version())
            install_log.write("Created registry value at: \"HKEY_CURRENT_USER\\SOFTWARE\\OBA Otomatik Oynatici\\version\"")

        except PermissionError as exc:
            install_log.write(f"An error occured due to system permissions:\n{format_exc()}\n")
            MessageBox(0,"Yetki hatası. Uygulamayı yönetici olarak çalıştırmayı deneyin.", "ÖBA Otomatik Oynatıcı | Kurulum", MB_OK | MB_ICONERROR)
            exit(1)

        except Exception as exc:
            exc_tb = format_exc()
            install_log.write(f"An unexpected error occured:\n{exc_tb}\n")
            MessageBox(0,f"Beklenmedik bir hata oluştu:\n\n{exc_tb}", "ÖBA Otomatik Oynatıcı | Kurulum", MB_OK | MB_ICONERROR)
            exit(1)

        else:
            install_log.write("Installation completed without any issues.")

    else:  
        
        updater_log = Log("Updater")
        updater_log.write("Getting version information from Github...")

        CONTINUE_UPDATE = False
        try:
            local_version = read_key(HKEY_CURRENT_USER,"SOFTWARE\\OBA Otomatik Oynatici","version")
            main_version = get_version()
        except Exception as exc:
            exc_type = exc.__class__.__name__.lower()
            updater_log.write(f"An error occured while getting version information:\n{format_exc()}\n")

            if exc_type == "sslerror":
                req_without_verify = MessageBox(0,"Sunucu ile SSL sertifikası doğrulaması başarısız oldu. SSL sertifika doğrulamasını pas geçip gene de güncellemeye devam etmek istiyor musunuz?\n\n(Bu durum güvenlik açıklarına sebep olabileceğinden tavsiye edilmez.)", "ÖBA Otomatik Oynatıcı | Güncelleme Sistemi", MB_YESNO | MB_ICONERROR)

                if req_without_verify == 6:
                    VERIFICATE_SSL = False
                    updater_log.write("Attempting again to get version information from Github...")
                    try:
                        content_bytes = get_program_contents(timeout=3, verify=VERIFICATE_SSL)
                    except Exception as exc:
                        updater_log.write(f"Attempt failed:\n{format_exc()}\n")
                    else:
                        CONTINUE_UPDATE = True
        else:
            CONTINUE_UPDATE = True


        if CONTINUE_UPDATE:
            if local_version != main_version:
                updater_log.write("Application isn't up to date.")
                try:
                    if any(b"oba_gui" in i for i in process_list()):
                        kill("oba_gui.exe")
                        updater_log.write("Killed 'oba_gui.exe'")

                    updater_log.write("Getting app contents from Github...")
                    content_bytes = get_program_contents(timeout=3,verify=VERIFICATE_SSL)
                    
                    updater_log.write(f"Creating temporary folder: \"{TEMP_PATH}\"")
                    create_dir(TEMP_PATH)

                    updater_log.write("Downloading app contents...")
                    write_byte(f"{TEMP_PATH}\\executable.zip","wb",content_bytes)
                    updater_log.write("App contents have downloaded.")

                    updater_log.write("App folder is cleaning...")
                    removeall(PROGRAM_PATH)
                    create_dir(PROGRAM_PATH)
                    updater_log.write("App folder been cleaned.")
                     
                    updater_log.write("Extracting contents from temporary zip file...")
                    extract(f"{TEMP_PATH}\\executable.zip",PROGRAM_PATH)
                    updater_log.write("Contents have extracted from zip file.")

                    updater_log.write("Deleting temporary folder...")
                    removeall(TEMP_PATH)
                    updater_log.write("Temporary folder been deleted.")
                    
                    updater_log.write("Updating registry value at: \"HKEY_CURRENT_USER\\SOFTWARE\\OBA Otomatik Oynatici\\version\"")
                    create_key(HKEY_CURRENT_USER,"SOFTWARE\\OBA Otomatik Oynatici","version",get_version())
                    updater_log.write("Updated registry value at: \"HKEY_CURRENT_USER\\SOFTWARE\\OBA Otomatik Oynatici\\version\"")

                except PermissionError as exc:
                    MessageBox(0,"Yetki hatası. Uygulamayı yönetici olarak çalıştırmayı deneyin.", "ÖBA Otomatik Oynatıcı | Güncelleme Sistemi", MB_OK | MB_ICONERROR)
                    exit(1)

                except Exception as exc:
                    exc_tb = format_exc()
                    MessageBox(0,f"Beklenmedik bir hata oluştu:\n\n{exc_tb}", "ÖBA Otomatik Oynatıcı | Güncelleme Sistemi", MB_OK | MB_ICONERROR)
                    exit(1)

                else:
                    updater_log.write("Update completed without any issues.")
                    
            elif local_version == main_version:
                updater_log.write("Application is already up to date.")
                updater_log.open()
                

    if not any(b"oba_gui" in i for i in process_list()):
        start(f"{PROGRAM_PATH}\\oba_gui.exe")

    exit(0)
        

    
    
