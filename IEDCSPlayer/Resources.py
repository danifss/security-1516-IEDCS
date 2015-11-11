import os


serverIp = "localhost"
serverPort = "8000"
serverUrl = "http://" + serverIp + ":" + serverPort

class api:
    HOMEPAGE = serverUrl + "/iedcs/"
    LOGIN = serverUrl + "/api/user/login/"
    GETCONTENTBYUSER = serverUrl + "/api/content/user/"


# color
class co:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

