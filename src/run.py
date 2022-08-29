from os import path, environ, mkdir, remove, rmdir, listdir
from sys import exit
from time import strftime
from requests import Session
from utils.exceptions import FailedRequestError
from utils.process import *
from utils.env_paths import *
from utils import Log
from zipfile import ZipFile
from threading import Thread
from winreg import CreateKeyEx, SetValueEx, QueryValueEx, OpenKeyEx, HKEY_CURRENT_USER, KEY_WRITE, KEY_READ, REG_SZ
from win32api import MessageBox
from win32con import MB_ICONERROR, MB_OK

class Setup:
    @staticmethod
    def is_installed():
        try:
            Updater.get_local_version()
        except FileNotFoundError: return False
        else: return True

    @staticmethod   
    def download_packages(folder_path):
        try:
            with Session() as session:
                executable_request = session.get("https://github.com/MehmetKLl/OBA-Otomatik-Oynatici/raw/main/dist/executable.zip")
                executable_filebytes = executable_request.content
                
        except:
            raise FailedRequestError()
        else:
            if not path.exists(folder_path):
                mkdir(folder_path)
                
            with open(f"{folder_path}\\executable.zip","wb") as file_event:
                file_event.write(executable_filebytes)
                

    @staticmethod
    def install_packages(folder_path,zip_path):
        if not path.exists(folder_path):
            mkdir(folder_path)
        
        with ZipFile(f"{zip_path}\\executable.zip","r") as file_event:
            file_event.extractall(f"{folder_path}")

        with CreateKeyEx(HKEY_CURRENT_USER,"SOFTWARE\\OBA Otomatik Oynatici",0,KEY_WRITE) as key:
            SetValueEx(key,"version",0,REG_SZ,f"{Updater.get_version()}")

    @staticmethod
    def delete_packages(folder_path):
        remove(f"{folder_path}\\executable.zip")
        rmdir(f"{folder_path}")

class Updater:
    @staticmethod
    def get_version(timeout=3):
        try:
            with Session() as session:
                request = session.get("https://raw.githubusercontent.com/MehmetKLl/OBA-Otomatik-Oynatici/main/VERSION",timeout=timeout)
                version = request.text.replace("\n","")
        except Exception as err:
            raise FailedRequestError(err)
        else:
            return version

    @staticmethod
    def get_local_version():
        with OpenKeyEx(HKEY_CURRENT_USER,"SOFTWARE\\OBA Otomatik Oynatici",0,KEY_READ) as key:
            version = QueryValueEx(key,"version")
        return version[0]

    @staticmethod
    def delete_files(folder_path):
        absolute_path = path.abspath(folder_path)
        folder_contents = listdir(absolute_path)
        for folder_content in folder_contents:
            if path.isdir(f"{absolute_path}\\{folder_content}"):
                Updater.delete_files(f"{absolute_path}\\{folder_content}")
                rmdir(f"{absolute_path}\\{folder_content}")
            else:
                remove(f"{absolute_path}\\{folder_content}")

    @staticmethod
    def download_packages(folder_path):
        try:
            with Session() as session:
                request = session.get("https://github.com/MehmetKLl/OBA-Otomatik-Oynatici/raw/main/dist/executable.zip")
                package_bytes = request.content
        except Exception as err:
            raise FailedRequestError(err)
        else:
            if not path.exists(f"{folder_path}"):
                mkdir(f"{folder_path}")
            with open(f"{folder_path}\\update_package.zip","wb") as file_event:
                file_event.write(package_bytes)

    @staticmethod
    def install_packages(folder_path,zip_path):
            with ZipFile(f"{zip_path}\\update_package.zip","r") as file_event:
                file_event.extractall(f"{folder_path}")

    @staticmethod
    def remove_packages(folder_path):
            remove(f"{folder_path}\\update_package.zip")

    @staticmethod
    def update_version():
        with CreateKeyEx(HKEY_CURRENT_USER,"SOFTWARE\\OBA Otomatik Oynatici",0,KEY_WRITE) as key:
                SetValueEx(key,"version",0,REG_SZ,f"{Updater.get_version()}")

if __name__ == "__main__":
    if not Setup.is_installed():
        try:
            Setup.download_packages(SETUP_PATH)
            Setup.install_packages(PROGRAM_PATH,SETUP_PATH)
            Setup.delete_packages(SETUP_PATH)
        except FailedRequestError:
            MessageBox(0,"İnternet bağlantınız yavaş veya mevcut olmadığından program kurulamadı.","ÖBA Otomatik Oynatıcı", MB_OK | MB_ICONERROR)
            exit(1)
        except PermissionError:
            MessageBox(0,"Yetki hatası. Programı yönetici olarak çalıştırmayı deneyin.","ÖBA Otomatik Oynatıcı", MB_OK | MB_ICONERROR)
            exit(1)
        except Exception as err:
            MessageBox(0,f"Beklenmedik hata: {err}","ÖBA Otomatik Oynatıcı", MB_OK | MB_ICONERROR)
            exit(1)
        else:
            run(f"{PROGRAM_PATH}",f"oba_gui.exe")
            exit(0)
    else:
        updater_log = Log(f"updater.exe {strftime('%d.%m.%Y %H.%M.%S')}")
        try:
            main_version = Updater.get_version()
            user_version = Updater.get_local_version()
        except FailedRequestError:
            updater_log.write("İnternet mevcut değil.","warning")
            if not any(["oba_gui.exe" in i for i in process_list()]):
                run(f"\"{PROGRAM_PATH}\\oba_gui.exe\"",f"{PROGRAM_PATH}")
            exit(0)
        else:
            if user_version != main_version:
                kill("oba_gui.exe")
                updater_log.write("Güncelleme başlatılıyor...","info")
                Updater.download_packages(TEMP_PATH)
                updater_log.write("Dosyalar yüklendi!","info")
                updater_log.write("Dosyalar çıkartılıyor...","info")
                Updater.delete_files(PROGRAM_PATH)
                Updater.install_packages(PROGRAM_PATH,TEMP_PATH)
                Updater.remove_packages(TEMP_PATH)
                Updater.update_version()
                updater_log.write("Güncelleme başarılı.","info")
                run(f"{PROGRAM_PATH}",f"oba_gui.exe")
            else:
                updater_log.write("Uygulama güncel.","info")
                if not any(["oba_gui.exe" in i for i in process_list()]):
                    run(f"{PROGRAM_PATH}",f"oba_gui.exe")
            exit(0)
    
    
    
