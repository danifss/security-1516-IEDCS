# import os


serverIp = "localhost"
serverPort = "8000"
serverUrl = "https://" + serverIp + ":" + serverPort

class api:
    HOMEPAGE = serverUrl + "/"
    LOGIN = serverUrl + "/api/user/login/"
    GET_CONTENT_BY_USER = serverUrl + "/api/content/user/"
    GET_CONTENT_TO_PLAY = serverUrl + "/api/content/play/"
    GET_CONTENT_PAGES = serverUrl + "/api/content/pages/"
    CHALLENGE = serverUrl + "/api/content/challenge/"
    HAS_CONTENT_TO_PLAY = serverUrl + "/api/content/hascontent/"
    # GET_CONTENT_FILENAME = serverUrl + "/api/content/name/"
    # GET_CONTENT_FILEPATH = serverUrl + "/api/content/filepath/"
    GET_DEVICE = serverUrl + "/api/device/"
    SAVE_DEVICE = serverUrl + "/api/device/new/"

# colors
class co:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

