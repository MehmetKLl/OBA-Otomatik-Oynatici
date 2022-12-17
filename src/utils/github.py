from requests import Session
from . import constants

def get_version(timeout=3,verify=True):
    with Session() as session:
        request = session.get(constants.GitHub.VERSION_URL,timeout=timeout,verify=verify)
        version = request.text.replace("\n","")
    return version

def get_program_contents(timeout=3,verify=True):
    with Session() as session:
        executable_request = session.get(constants.GitHub.EXECUTABLE_URL,timeout=timeout,verify=verify)
        filebytes = executable_request.content
    return filebytes
