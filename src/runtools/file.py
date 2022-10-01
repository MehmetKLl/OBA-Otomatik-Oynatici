from zipfile import ZipFile
from os import path, mkdir, rmdir
from shutil import rmtree


def extract(file,destination):
    with ZipFile(file,"r") as zip_file:
        zip_file.extractall(destination)

def removeall(target_path):
    absolute_path = path.abspath(target_path)
    rmtree(absolute_path)

def remove_dir(folder):
    rmdir(folder)

def create_dir(folder):
    if not path.exists(folder):
        mkdir(folder)

def write_byte(file,mode,bytes_:bytes):
    with open(file,mode) as file_io:
        file_io.write(bytes_)


