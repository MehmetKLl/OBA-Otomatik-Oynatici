from utils.version_controller import *
from utils.env_paths import *
from utils import Log
from utils.exceptions import FailedRequestError
from utils import process_list
from subprocess import call, CREATE_NO_WINDOW
from threading import Thread


if __name__ == "__main__":
    updater_log = Log()
    try:
        main_version = get_version()
        user_version = get_local_version()
    except FailedRequestError:
        updater_log.write("İnternet mevcut değil.","warning")
        if not any(["oba_gui.exe" in i for i in process_list()]):
            Thread(target=lambda:call(f"\"{PROGRAM_PATH}\\main\\oba_gui.exe\"",shell=False,creationflags=CREATE_NO_WINDOW,cwd=f"{PROGRAM_PATH}\\main")).start()
    else:
        if user_version != main_version:
            call(["taskkill","-f","-im","oba_gui.exe","-t"],shell=False,creationflags=CREATE_NO_WINDOW)
            updater_log.write("Güncelleme başlatılıyor...","info")
            download_packages(TEMP_PATH)
            updater_log.write("Dosyalar yüklendi!","info")
            updater_log.write("Dosyalar çıkartılıyor...","info")
            install_packages(PROGRAM_PATH,TEMP_PATH)
            updater_log.write("Güncelleme başarılı.","info")
            Thread(target=lambda:call(f"\"{PROGRAM_PATH}\\main\\oba_gui.exe\"",shell=False,creationflags=CREATE_NO_WINDOW,cwd=f"{PROGRAM_PATH}\\main")).start()
        else:
            updater_log.write("Uygulama güncel.","info")
            if not any(["oba_gui.exe" in i for i in process_list()]):
                Thread(target=lambda:call(f"\"{PROGRAM_PATH}\\main\\oba_gui.exe\"",shell=False,creationflags=CREATE_NO_WINDOW,cwd=f"{PROGRAM_PATH}\\main")).start()
