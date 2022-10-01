from winreg import HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER, HKEY_CLASSES_ROOT, OpenKeyEx, CreateKeyEx, QueryValueEx, SetValueEx, KEY_READ, KEY_WRITE, REG_SZ

def read_key(hkey,key_location,value_name):
    with OpenKeyEx(hkey,key_location,0,KEY_READ) as key:
            version = QueryValueEx(key,value_name)
    return version[0]

def create_key(hkey,key_location,value_name,value):
    with CreateKeyEx(hkey,key_location,0,KEY_WRITE) as key:
        SetValueEx(key,value_name,0,REG_SZ,value)

def check_key(hkey,key_location,value_name):
    try:
        with OpenKeyEx(hkey,key_location,0,KEY_READ) as key:
            version = QueryValueEx(key,value_name)
    except FileNotFoundError:
        return False

    return True
