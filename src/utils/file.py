from zipfile import ZipFile
from os import path, makedirs, rmdir, remove, listdir
from shutil import rmtree


def extract(file,destination):
    with ZipFile(file,"r") as zip_file:
        zip_file.extractall(destination)

def remove_all(target_path):
    target_path = target_path.strip("\\")
    absolute_path = path.abspath(target_path)
    rmtree(absolute_path)

def remove_in(target_path):
    target_path = path.abspath(target_path.strip("\\"))
    
    for content in listdir(target_path):
        content_abs_path = f"{target_path}\\{content}"

        if path.isfile(content_abs_path):
            remove(content_abs_path)
        
        elif path.isdir(content_abs_path):
            remove_in(content_abs_path)
            rmdir(content_abs_path)
        

        

def remove_folder(folder):
    rmdir(folder)

def create_folder(folder):
    return makedirs(folder, exist_ok=True)

def write_byte(file,bytes_:bytes):
    with open(file,"wb") as file_io:
        file_io.write(bytes_)
        
        
