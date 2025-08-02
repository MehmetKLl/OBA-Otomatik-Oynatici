from winreg import OpenKeyEx, CreateKeyEx, DeleteValue, QueryValueEx, SetValueEx, KEY_READ, KEY_WRITE, REG_SZ, HKEY_CURRENT_USER
from .constants import Registry

def read_key(hkey,key_location,value_name):
    with OpenKeyEx(hkey,key_location,0,KEY_READ) as key:
            value = QueryValueEx(key,value_name)

    return value[0]

def create_key(hkey,key_location,value_name,value):
    with CreateKeyEx(hkey,key_location,0,KEY_WRITE) as key:
        SetValueEx(key,value_name,0,REG_SZ,value)

def delete_key(hkey,key_location,value_name):
    with OpenKeyEx(hkey,key_location,0,KEY_WRITE) as key:
        DeleteValue(key, value_name)

def check_key_exists(hkey,key_location,value_name):
    try:
        with OpenKeyEx(hkey,key_location,0,KEY_READ) as key:
            QueryValueEx(key,value_name)
    except FileNotFoundError:
        return False

    return True

def check_is_first_use():
    return check_key_exists(HKEY_CURRENT_USER, Registry.KEY_PATH, Registry.FIRSTUSE_KEY_NAME)

def delete_first_use_key():
    return delete_key(HKEY_CURRENT_USER, Registry.KEY_PATH, Registry.FIRSTUSE_KEY_NAME)