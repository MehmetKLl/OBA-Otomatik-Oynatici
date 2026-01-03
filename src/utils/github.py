from requests import Session
from . import constants
from json import loads

def get_version(timeout=3,verify=True):
    with Session() as session:
        request = session.get(constants.GitHub.LATEST_RELEASE_URL, timeout = timeout, verify = verify)
        latest_release_information = loads(request.text)

    return latest_release_information["name"].split("v")[1]

def get_program_contents(version = "latest", timeout = 3, verify = True):
    with Session() as session:
        executable_request = session.get(f"https://github.com/MehmetKLl/OBA-Otomatik-Oynatici/releases/latest/download/x86.zip" if version == "latest" else f"https://github.com/MehmetKLl/OBA-Otomatik-Oynatici/releases/download/v{version}/x86.zip", timeout = timeout, verify = verify)
        filebytes = executable_request.content

    return filebytes

def get_bootstrapper_contents(version = "latest", timeout = 3, verify = True):
    with Session() as session:
        executable_request = session.get(f"https://github.com/MehmetKLl/OBA-Otomatik-Oynatici/releases/latest/download/oba_otomatik_oynatma.zip" if version == "latest" else f"https://github.com/MehmetKLl/OBA-Otomatik-Oynatici/releases/download/v{version}/oba_otomatik_oynatma.zip", timeout = timeout, verify = verify)
        filebytes = executable_request.content

    return filebytes