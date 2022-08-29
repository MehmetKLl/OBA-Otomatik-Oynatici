from tkinter import messagebox, Tk, Label, Frame, StringVar, BooleanVar, Toplevel
from tkinter.ttk import Button, Checkbutton, Entry
from multiprocessing import freeze_support
from threading import Thread
from keyboard import is_pressed
from utils import Process, main, exceptions
from requests import Session
from winreg import OpenKeyEx, HKEY_CURRENT_USER, KEY_READ, QueryValueEx

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

class Root(Tk):
    def __init__(self):
        super().__init__()
        self.setup()
        self.place_elements()
        self.mainloop()

    def setup(self):
        self.geometry("450x400")
        self.resizable(False,False)
        self.title("ÖBA Otomatik Oynatıcı v1.3.1")
        self.iconbitmap("oba.ico")
        self.is_settings_opened = False
        self.shortcut, self.autoclose, self.devmode = StringVar(), BooleanVar(), BooleanVar()
        self.shortcut.set("CTRL+ESC")
        self.autoclose.set(True) 
        self.devmode.set(False)
        

    def create_box(self, title, text, charlimit):
        frame = Frame(self)
        title = Label(frame,text=title,justify="left")
        text_box = Label(frame,text="\n".join([text[i:i+charlimit] for i in range(0,len(text),charlimit)]),justify="left",bg="white")
        title.grid(row=0,column=1,ipady=2,ipadx=2,sticky="w")
        text_box.grid(row=1,column=1,pady=0,ipady=5,ipadx=5)
        return frame
    
    def place_elements(self):
        self.create_box("Hakkında","ÖBA Otomatik Oynatıcı, basit bir makro uygulamasıdır. Dışarı çıkacağınız vakit programı açık bırakabilirsiniz. Program sunucu tarafında işlem yapmamakta ve sadece görüntü işleme yapmaktadır.",72).grid(row=0,column=0,padx=(10,0),pady=(20,0),sticky="w")
        self.create_box("Kullanım","Programı başlat tuşuna basarak çalıştırabilirsiniz. Program çalıştırıldığında otomatik olarak arayüz kaybolacaktır. Program çalıştırıldığı vakit ekranda Chrome tarayıcısında \"Eğitime devam et\" butonundan sonra açılan kısım %100 büyütme boyutunda görüntüsü bulunmalıdır. Programı istediğiniz zaman ayarladığınız kısayol ile durdurabilirsiniz.",72).grid(row=1,column=0,padx=(10,),pady=(10,0),sticky="w")
        
        self.footer = Frame(width=400)
        self.footer.grid(row=2,column=0,pady=(50,0),padx=(10,0),sticky="w")
        self.start_button = Button(self.footer,text="Başlat",command=self.start)
        self.start_button.grid(row=0,column=0)
        self.settings_button = Button(self.footer,text="Ayarlar",command=self.open_settings)
        self.settings_button.grid(row=0,column=1,padx=5)
        

    def open_settings(self):
        if not self.is_settings_opened:
            SettingsWidget(self)
        else:
            messagebox.showerror("Ayarlar","Ayarlar sekmesi zaten açık.")
    
    def start(self):
        if self.autoclose.get():
            self.wm_attributes("-alpha",0)
        Thread(target=self._start).start()
        
    
    def _start(self):
        process = Process(target=main)
        process.start()
        self.start_button.config(state="disabled")
        while True:
            if self.test_key():
                if process.exception:
                    messagebox.showerror("ÖBA Otomatik Oynatıcı v1.3.0",f"Hata yakalandı:\n\n{process.exception[1]}" if self.devmode.get() else "Programda hata oluştu ve program sonlandırıldı.")
                    process.terminate()
                    self.wm_attributes("-alpha",1)
                    break
                if is_pressed(self.shortcut.get()):
                    messagebox.showinfo("ÖBA Otomatik Oynatıcı v1.3.0","Program sonlandırıldı.")
                    process.terminate()
                    self.wm_attributes("-alpha",1)
                    break
            else:
                messagebox.showinfo("ÖBA Otomatik Oynatıcı v1.3.0","Atadığınız kısayol geçersiz.")
                break
        self.start_button.config(state="normal")
    
    def test_key(self):
        try:
            is_pressed(self.shortcut.get())
        except:
            return False
        else:
            return True
            
        
    
class SettingsWidget(Toplevel):
    def __init__(self,obj):
        super().__init__(obj)
        self.setup(obj)
        
    def setup(self,obj):
        obj.is_settings_opened = True
        self.transient(obj)
        self.geometry("275x350")
        self.title("ÖBA Otomatik Oynatıcı v1.3.1")
        self.iconbitmap("oba.ico")
        self.resizable(False,False) 
        self.protocol("WM_DELETE_WINDOW",lambda:self.settings_destroy(obj))
        self.place_elements(obj)
            
    def settings_destroy(self,obj):
        self.destroy()
        obj.is_settings_opened = False

    def place_elements(self,obj):
        shortcut_frame = Frame(self)
        shortcut_frame.grid(row=0,column=0,padx=(10,0),pady=(20,0),sticky="w")
        shortcut_title = Label(shortcut_frame,text="Programı durdurma kısayolu:",justify="left")
        shortcut_title.grid(row=0,column=0,pady=(0,5))
        shortcut_entry = Entry(shortcut_frame,justify="left",textvariable=obj.shortcut)
        shortcut_entry.grid(row=1,column=0,sticky="w")
        
        autoclose_frame = Frame(self)
        autoclose_frame.grid(row=1,column=0,padx=(10,0),pady=(10,0),sticky="w")
        autoclose_title = Label(autoclose_frame,text="Otomatik kapanma ayarı:",justify="left")
        autoclose_title.grid(row=0,column=0,pady=(0,2.5))
        autoclose_checkbox = Checkbutton(autoclose_frame,text="Açık"
                                         if obj.autoclose.get() else
                                         "Kapalı",
                                         command=lambda:autoclose_checkbox.config(text="Açık") if obj.autoclose.get() else autoclose_checkbox.config(text="Kapalı"),
                                         variable=obj.autoclose,onvalue=True,offvalue=False
                                         )
        autoclose_checkbox.grid(row=1,column=0,sticky="w")
        
        devmode_frame = Frame(self)
        devmode_frame.grid(row=2,column=0,padx=(10,0),pady=(10,0),sticky="w",ipadx=2.5,ipady=2.5)
        devmode_title = Label(devmode_frame,text="Geliştirici modu:",justify="left")
        devmode_title.grid(row=0,column=0,pady=(0,2.5))
        devmode_checkbox = Checkbutton(devmode_frame,text="Açık"
                                         if obj.devmode.get() else
                                         "Kapalı",
                                         command=lambda:devmode_checkbox.config(text="Açık") if obj.devmode.get() else devmode_checkbox.config(text="Kapalı"),
                                         variable=obj.devmode,onvalue=True,offvalue=False
                                         )
        devmode_checkbox.grid(row=1,column=0,sticky="w")

        version_frame = Frame(self)
        version_frame.grid(row=3,column=0,padx=(10,0),pady=(10,0),sticky="w")
        version_label = Label(version_frame,text="Versiyon:",justify="left")
        version_label.grid(row=0,column=0,padx=(0,5))
        version_box = Entry(version_frame)
        version_box.insert(0,get_local_version())
        version_box.config(state="disabled")
        version_box.grid(row=0,column=1)
        check_version_button = Button(self,text="Güncelleştirmeleri denetle",command=self.check_version)
        check_version_button.grid(row=4,column=0,pady=(5,0),padx=(10,0),sticky="w")


    def check_version(self):
        try:
            local_version = get_local_version()
            version = get_version()
            if local_version == version:
                messagebox.showinfo("ÖBA Otomatik Oynatıcı v1.3.0",f"Programınız güncel.\n\nProgramın sürümü: v{local_version}\nEn son yayınlanan sürüm: v{version}")
            else:
                ask_for_update = messagebox.showinfo("ÖBA Otomatik Oynatıcı v1.3.0",f"Programınızın yeni bir sürümü bulunuyor.\n\nProgramın sürümü: v{local_version}\nEn son yayınlanan sürüm: v{version}\n\nProgramınızı en son sürüme güncellemek ister misinz?")
        except exceptions.FailedRequestError:
            messagebox.showwarning("ÖBA Otomatik Oynatıcı v1.3.0","Sunucu ile bağlantı kurulamadı.Bunun birkaç sebebi olabilir.\n\n• İnternet bağlantınız yok veya zayıf.\n• Sunucu kapalı veya istekleri reddediyor.\n• Aranan sunucu geçersiz.")

        

if __name__ == "__main__":
    freeze_support()
    Root()
