from requests import Session
from utils.exceptions import FailedRequestError

def get_version(timeout=3,verify=True):
    with Session() as session:
        request = session.get("https://raw.githubusercontent.com/MehmetKLl/OBA-Otomatik-Oynatici/main/VERSION",timeout=timeout,verify=verify)
        version = request.text.replace("\n","")
    return version

def get_program_contents(timeout=3,verify=True):
    with Session() as session:
        executable_request = session.get("https://github.com/MehmetKLl/OBA-Otomatik-Oynatici/raw/main/dist/executable.zip",timeout=timeout,verify=verify)
        filebytes = executable_request.content
    return filebytes
