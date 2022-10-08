from zipfile import ZipFile
from os import path, mkdir, rmdir
from shutil import rmtree


def extract(file,destination):
    with ZipFile(file,"r") as zip_file:
        zip_file.extractall(destination)

def remove_all(target_path):
    absolute_path = path.abspath(target_path)
    rmtree(absolute_path)

def remove_dir(folder):
    rmdir(folder)

def create_dir(folder):
    if not path.exists(folder):
        mkdir(folder)

def write_byte(file,bytes_:bytes):
    with open(file,"wb") as file_io:
        file_io.write(bytes_)
        
        
