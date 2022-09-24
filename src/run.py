from os import path, environ, mkdir, remove, rmdir, listdir
from traceback import format_exc
from sys import exit
from time import strftime
from requests import Session
from utils.exceptions import FailedRequestError
from utils.process import *
from utils.env_paths import *
from utils.log import *
from zipfile import ZipFile
from winreg import CreateKeyEx, SetValueEx, QueryValueEx, OpenKeyEx, HKEY_CURRENT_USER, KEY_WRITE, KEY_READ, REG_SZ
from win32api import MessageBox
from win32con import MB_ICONERROR, MB_OK

class Installer:
    def __init__(self):
        self.log = Log("Installer")

    def finish(self):
        self.log.close()

    def get_version(self,timeout=3):
        self.log.write("Getting version info from Github...")
        try:
            with Session() as session:
                request = session.get("https://raw.githubusercontent.com/MehmetKLl/OBA-Otomatik-Oynatici/main/VERSION",timeout=timeout)
                version = request.text.replace("\n","")
        except Exception as err:
            exc = format_exc()
            self.log.write(f"An error occured while getting version data from Github: \"\"\"{exc}\"\"\"")
            
            raise FailedRequestError(err)
        else:
            self.log.write("Successfully got version data from Github.")
            
            return version
    
    def check_registry(self):
        with OpenKeyEx(HKEY_CURRENT_USER,"SOFTWARE\\OBA Otomatik Oynatici",0,KEY_READ) as key:
            version = QueryValueEx(key,"version")
        return version[0]

    def is_installed(self):
        self.log.write(f"Checking if the application is installed on the system...")
        self.log.write(f"Checking registry key: \"HKEY_CURRENT_USER\\SOFTWARE\\OBA Otomatik Oynatici\"")
        try:
            self.check_registry()
        except FileNotFoundError:
            self.log.write("Couldn't find registry key: \"HKEY_CURRENT_USER\\SOFTWARE\\OBA Otomatik Oynatici\"")
            self.log.write("Application isn't installed on this system.")
            return False
        else:
            self.log.write("Registry key found: \"HKEY_CURRENT_USER\\SOFTWARE\\OBA Otomatik Oynatici\"")
            self.log.write("Application is already installed on this system.")
            return True
   
    def download_packages(self,folder_path):
        self.log.write("Downloading the application from \"https://github.com/MehmetKLl/OBA-Otomatik-Oynatici/raw/main/dist/executable.zip\"")
        try:
            with Session() as session:
                executable_request = session.get("https://github.com/MehmetKLl/OBA-Otomatik-Oynatici/raw/main/dist/executable.zip")
                executable_filebytes = executable_request.content
                
        except Exception as err:
            exc = format_exc()
            self.log.write(f"An error occured while downloading the package from Github: \n\"\"\"\n{exc}\n\"\"\"")
            raise FailedRequestError(err)
        else:
            self.log.write("File bytes successfully extracted from Github.")

            if not path.exists(folder_path):
                mkdir(folder_path)
                self.log.write(f"Folder created: \"{folder_path}\"")

            self.log.write("Writing file bytes to files...")
            with open(f"{folder_path}\\executable.zip","wb") as file_event:
                file_event.write(executable_filebytes)
                
            self.log.write("File bytes have been successfully written to files.")
                

    def install_packages(self,folder_path,zip_path):
        if not path.exists(folder_path):
            mkdir(folder_path)
            self.log.write(f"Folder created: \"{folder_path}\"")

        self.log.write("Extracting files from temporary zip file...")
        with ZipFile(f"{zip_path}\\executable.zip","r") as file_event:
            file_event.extractall(f"{folder_path}")

        self.log.write("Files have been successfully extracted from zip file.")

        self.log.write("Adding registry value to: \"HKEY_CURRENT_USER\\SOFTWARE\\OBA Otomatik Oynatici\\version\"")
        with CreateKeyEx(HKEY_CURRENT_USER,"SOFTWARE\\OBA Otomatik Oynatici",0,KEY_WRITE) as key:
            SetValueEx(key,"version",0,REG_SZ,f"{self.get_version()}")
            
        self.log.write("Registry value has been added.")

    def delete_packages(self,folder_path):
        self.log.write("Deleting temporary files...")
        remove(f"{folder_path}\\executable.zip")
        self.log.write("Temporary files been deleted.")
        self.log.write("Removing temporary folder...")
        rmdir(f"{folder_path}")
        self.log.write("Temporary folder been removed.")

class Updater:
    def __init__(self):
        self.log = Log("Updater")

    def finish(self):
        self.log.close()

    def get_version(self, timeout=3):
        self.log.write("Getting version info from Github...")
        try:
            with Session() as session:
                request = session.get("https://raw.githubusercontent.com/MehmetKLl/OBA-Otomatik-Oynatici/main/VERSION",timeout=timeout)
                version = request.text.replace("\n","")
        except Exception as err:
            exc = format_exc()
            self.log.write(f"An error occured while getting version data from Github: \"\"\"{exc}\"\"\"")
            
            raise FailedRequestError(err)
        else:
            self.log.write("Successfully got version data from Github.")
            
            return version

    def get_local_version(self):
        self.log.write(f"Reading registry value at: \"HKEY_CURRENT_USER\\SOFTWARE\\OBA Otomatik Oynatici\\version\"")
        with OpenKeyEx(HKEY_CURRENT_USER,"SOFTWARE\\OBA Otomatik Oynatici",0,KEY_READ) as key:
            version = QueryValueEx(key,"version")
        self.log.write("Successfully read local version from: \"HKEY_CURRENT_USER\\SOFTWARE\\OBA Otomatik Oynatici\\version\"")
        return version[0]

    
    def delete_files(self,folder_path):
        absolute_path = path.abspath(folder_path)
        folder_contents = listdir(absolute_path)
        for folder_content in folder_contents:
            if path.isdir(f"{absolute_path}\\{folder_content}"):
                self.delete_files(f"{absolute_path}\\{folder_content}")
                self.log.write(f"Removing \"{absolute_path}\\{folder_content}\"")
                rmdir(f"{absolute_path}\\{folder_content}")
                self.log.write(f"Successfully removed \"{absolute_path}\\{folder_content}\"")
            else:
                self.log.write(f"Deleting \"{absolute_path}\\{folder_content}\"")
                remove(f"{absolute_path}\\{folder_content}")
                self.log.write(f"Successfully deleted \"{absolute_path}\\{folder_content}\"")

    def download_packages(self, folder_path):
        self.log.write("Downloading the new version from \"https://github.com/MehmetKLl/OBA-Otomatik-Oynatici/raw/main/dist/executable.zip\"")
        try:
            with Session() as session:
                request = session.get("https://github.com/MehmetKLl/OBA-Otomatik-Oynatici/raw/main/dist/executable.zip")
                package_bytes = request.content
        except Exception as err:
            exc = format_exc()
            self.log.write(f"An error occured while downloading the package from Github: \n\"\"\"\n{exc}\n\"\"\"")
            
            raise FailedRequestError(err)
        else:
            self.log.write("File bytes successfully extracted from Github.")
            
            if not path.exists(f"{folder_path}"):
                mkdir(f"{folder_path}")
                self.log.write(f"Folder created: \"{folder_path}\"")

            self.log.write("Writing file bytes to files...")
            with open(f"{folder_path}\\update_package.zip","wb") as file_event:
                file_event.write(package_bytes)

            self.log.write("File bytes have been successfully written to files.")

    def install_packages(self, folder_path,zip_path):
        self.log.write("Extracting files from temporary zip file...")
        with ZipFile(f"{zip_path}\\update_package.zip","r") as file_event:
            file_event.extractall(f"{folder_path}")

        self.log.write("Files have been successfully extracted from zip file.")

    def remove_packages(self, folder_path):
        self.log.write("Deleting temporary files...")
        remove(f"{folder_path}\\update_package.zip")
        self.log.write("Temporary files been deleted.")

    def update_version(self):
        self.log.write("Updating version info at: \"HKEY_CURRENT_USER\\SOFTWARE\\OBA Otomatik Oynatici\\version\"")
        with CreateKeyEx(HKEY_CURRENT_USER,"SOFTWARE\\OBA Otomatik Oynatici",0,KEY_WRITE) as key:
            version = self.get_version()
            SetValueEx(key,"version",0,REG_SZ,f"{version}")
        self.log.write(f"Version info successfully updated to: \"{version}\"")

if __name__ == "__main__":
    installer = Installer()
    if not installer.is_installed():
        try:
            installer.download_packages(SETUP_PATH)
            installer.install_packages(PROGRAM_PATH,SETUP_PATH)
            installer.delete_packages(SETUP_PATH)
        except FailedRequestError:
            MessageBox(0,"İnternet bağlantınız yavaş veya mevcut olmadığından program kurulamadı.","ÖBA Otomatik Oynatıcı", MB_OK | MB_ICONERROR)
            installer.finish()
            exit(1)
        except PermissionError:
            exc = format_exc()
            MessageBox(0,"Yetki hatası. Programı yönetici olarak çalıştırmayı deneyin.","ÖBA Otomatik Oynatıcı", MB_OK | MB_ICONERROR)
            installer.log.write("An error occured due to system permissions: \n\"\"\"\n{exc}\n\"\"\"")
            installer.finish()
            exit(1)
        except Exception as err:
            exc = format_exc()
            MessageBox(0,f"Beklenmedik hata:\n\n{exc}","ÖBA Otomatik Oynatıcı", MB_OK | MB_ICONERROR)
            installer.log.write("An unexpected error occured: \n\"\"\"\n{exc}\n\"\"\"")
            installer.finish()
            exit(1)
        else:
            start(f"{PROGRAM_PATH}\\oba_gui.exe")
            installer.finish()
            exit(0)
    else:
        updater = Updater()
        try:
            main_version = updater.get_version()
            user_version = updater.get_local_version()
        except FailedRequestError:
            if not any([b"oba_gui.exe" in i for i in process_list()]):
                start(f"{PROGRAM_PATH}\\oba_gui.exe")
            updater.finish()
            exit(0)
        else:
            if user_version != main_version:
                kill("oba_gui.exe")
                updater.download_packages(TEMP_PATH)
                updater.delete_files(PROGRAM_PATH)
                updater.install_packages(PROGRAM_PATH,TEMP_PATH)
                updater.remove_packages(TEMP_PATH)
                updater.update_version()
                start(f"{PROGRAM_PATH}\\oba_gui.exe")
            else:
                if not any([b"oba_gui.exe" in i for i in process_list()]):
                    start(f"{PROGRAM_PATH}\\oba_gui.exe")
            updater.finish()
            exit(0)
    
    
    
