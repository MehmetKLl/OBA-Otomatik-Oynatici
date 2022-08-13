from os import remove, rmdir, mkdir, listdir, path
from json import loads
from requests import Session
from zipfile import ZipFile
from utils.exceptions import *
from winreg import OpenKeyEx, HKEY_CURRENT_USER, KEY_READ, KEY_WRITE, QueryValueEx, CreateKeyEx, SetValueEx, REG_SZ


def get_version(timeout=3):
    try:
        with Session() as session:
            request = session.get("https://raw.githubusercontent.com/MehmetKLl/OBA-Otomatik-Oynatici/main/VERSION",timeout=timeout)
            version = request.text.replace("\n","")
    except Exception as err:
        raise FailedRequestError(err)
    else:
        return version

def get_local_version():
    with OpenKeyEx(HKEY_CURRENT_USER,"SOFTWARE\\OBA Otomatik Oynatici",0,KEY_READ) as key:
        version = QueryValueEx(key,"version")
    return version[0]

def delete_files(folder_path):
    absolute_path = path.abspath(folder_path)
    folder_contents = listdir(absolute_path)
    for folder_content in folder_contents:
        if path.isdir(f"{absolute_path}\\{folder_content}"):
            delete_files(f"{absolute_path}\\{folder_content}")
            rmdir(f"{absolute_path}\\{folder_content}")
        else:
            remove(f"{absolute_path}\\{folder_content}")



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

def install_packages(folder_path,zip_path):
        delete_files(f"{folder_path}\\main")
        with ZipFile(f"{zip_path}\\update_package.zip","r") as file_event:
            file_event.extractall(f"{folder_path}\\main")

        with CreateKeyEx(HKEY_CURRENT_USER,"SOFTWARE\\OBA Otomatik Oynatici",0,KEY_WRITE) as key:
            SetValueEx(key,"version",0,REG_SZ,f"{get_version()}")

        remove(f"{zip_path}\\update_package.zip")

  
