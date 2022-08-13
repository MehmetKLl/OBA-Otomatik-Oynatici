from os import path, environ, mkdir, remove, rmdir
from requests import Session
from utils.exceptions import FailedRequestError
from utils.version_controller import get_local_version, get_version
from utils.env_paths import *
from zipfile import ZipFile
from subprocess import call, CREATE_NO_WINDOW
from threading import Thread
from winreg import CreateKeyEx, SetValueEx, HKEY_CURRENT_USER, KEY_WRITE, REG_SZ
from win32api import MessageBox
from win32con import MB_ICONERROR, MB_OK


def is_installed():
    try:
        get_local_version()
    except: return False
    else: return True

def download_packages(folder_path):
    try:
        with Session() as session:
            executable_request = session.get("https://github.com/MehmetKLl/OBA-Otomatik-Oynatici/raw/main/dist/executable.zip")
            executable_filebytes = executable_request.content
            
            updater_request = session.get("https://github.com/MehmetKLl/OBA-Otomatik-Oynatici/raw/main/dist/updater_package.zip")
            updater_filebytes = updater_request.content
    except:
        raise FailedRequestError()
    else:
        if not path.exists(folder_path):
            mkdir(folder_path)
            
        with open(f"{folder_path}\\executable.zip","wb") as file_event:
            file_event.write(executable_filebytes)
            
        with open(f"{folder_path}\\updater.zip","wb") as file_event:
            file_event.write(updater_filebytes)

def install_packages(folder_path,zip_path):
    if not path.exists(folder_path):
        mkdir(folder_path)
        
    with ZipFile(f"{zip_path}\\updater.zip","r") as file_event:
        file_event.extractall(f"{environ['PROGRAMFILES(x86)']}\\OBA Otomatik Oynatici")

    if not path.exists(f"{folder_path}\\main"):   
        mkdir(f"{folder_path}\\main")
    
    with ZipFile(f"{zip_path}\\executable.zip","r") as file_event:
        file_event.extractall(f"{folder_path}\\main")

    with CreateKeyEx(HKEY_CURRENT_USER,"SOFTWARE\\OBA Otomatik Oynatici",0,KEY_WRITE) as key:
        SetValueEx(key,"version",0,REG_SZ,f"{get_version()}")

def delete_packages(folder_path):
    remove(f"{folder_path}\\updater.zip")
    remove(f"{folder_path}\\executable.zip")
    rmdir(f"{folder_path}")

def run(executable_path):
    Thread(target=lambda:call([f"{executable_path}\\updater.exe"],shell=False,creationflags=CREATE_NO_WINDOW,cwd=executable_path)).start()

if __name__ == "__main__":
    if not is_installed():
        try:
            download_packages(SETUP_PATH)
            install_packages(PROGRAM_PATH,SETUP_PATH)
            delete_packages(SETUP_PATH)
        except FailedRequestError:
            MessageBox(0,"İnternet bağlantınız yavaş veya mevcut olmadığından program kurulamadı.","ÖBA Otomatik Oynatıcı", MB_OK | MB_ICONERROR)
        except PermissionError:
            MessageBox(0,"Yetki hatası. Programı yönetici olarak çalıştırmayı deneyin.","ÖBA Otomatik Oynatıcı", MB_OK | MB_ICONERROR)
        except Exception as err:
            MessageBox(0,f"Beklenmedik hata: {err}","ÖBA Otomatik Oynatıcı", MB_OK | MB_ICONERROR)
            raise
        else:
            run(PROGRAM_PATH)
    else:
        run(PROGRAM_PATH)
    
    
    
