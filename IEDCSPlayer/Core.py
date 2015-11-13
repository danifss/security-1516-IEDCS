from Resources import *
from CryptoModule import *
import sys
import requests
import json


class Core(object):
    userID = "1"
    username = "daniel"
    password = "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4"
    email = "daniel.silva@ua.pt"
    firstName = "Daniel"
    lastName = "Silva"
    createdOn = "06/11/2015"
    loggedIn = False

    def __init__(self):

        self.crypt = CryptoModule()

        while not self.loggedIn:
            # user mut be logged in
            self.login()
            if not self.loggedIn:
                op = raw_input("\tExit?(y/N) ")
                if op == 'y':
                    print co.BOLD + co.HEADER + "\nTerminated by user! See you soon.\n"
                    sys.exit(0)
        ### print welcome message
        print co.HEADER+"\tWelcome "+co.BOLD+self.firstName+" "+self.lastName+co.ENDC


    ### Login
    def login(self):
        print co.BOLD + co.OKBLUE + "\n\n\t\t  Logging into IEDCS Player" + co.ENDC
        print co.WARNING
        username = raw_input("\tUsername: ")
        passwd = raw_input("\tPassword: ")
        print co.ENDC
        try:
            ### TODO send also device id in order to server check if the player is associated with this device
            hash_pass = self.crypt.hashingSHA256(passwd)
            result = requests.get(api.LOGIN+"?username="+username+"&password="+hash_pass, verify=True)


        except requests.ConnectionError:
            print co.FAIL+"Error connecting with server!\n"+co.ENDC
            return
        if result.status_code == 200:
            res = json.loads(result.text)
            self.username = username
            self.userID = res['id']
            self.email = res['email']
            self.firstName = res['first_name']
            self.lastName = res['last_name']
            self.loggedIn = True

            # if everything ok, lets generate device key or not
            print
            self.generateDevice()
        else:
            print co.FAIL+"\tFail doing log in. Error: "+str(result.status_code)+co.ENDC



    ### Logout
    def logout(self):
        self.userID = self.username = self.email = self.firstName = self.lastName = ""
        self.loggedIn = False
        print co.WARNING + "Logged out with success." + co.ENDC


    ### List content from logged user
    def list_my_content(self):
        try:
            result = requests.get(api.GETCONTENTBYUSER+str(self.userID), verify=True)
            if result.status_code == 200:
                res = json.loads(result.text)['results']
                if len(res) > 0:
                    print co.OKBLUE+co.BOLD+"\tThis is your content:\n"+co.ENDC
                    print co.HEADER+co.BOLD+"  ID  \t   Date of purchase\t\t    Name of product"+co.ENDC
                    distinct = []
                    for item in res:
                        if item not in distinct:
                            distinct += [item]
                            print co.OKGREEN+str(item['contentID'])+"\t"+item['createdOn']+"\t"+item['name']+co.ENDC
                else:
                    print co.HEADER+co.BOLD+"\tYou need to buy something!"+co.ENDC

        except requests.ConnectionError:
            print co.FAIL+"Error connecting with server!\n"+co.ENDC
            return

    ### Play content bought by the logged client
    def play_my_content(self, contentID):
        print "Showing content"


    ### Show personal information
    def show_my_info(self):
        print co.HEADER+co.BOLD+"Username  : "+co.ENDC+ \
              co.OKGREEN+self.username+co.ENDC
        print co.HEADER+co.BOLD+"Email     : "+co.ENDC+ \
              co.OKGREEN+self.email+co.ENDC
        print co.HEADER+co.BOLD+"First Name: "+co.ENDC+ \
              co.OKGREEN+self.firstName+co.ENDC
        print co.HEADER+co.BOLD+"Last Name : "+co.ENDC+ \
              co.OKGREEN+self.lastName+co.ENDC

    # generates device key if first run
    def generateDevice(self):
        print "generating device key"

        hashdevice = self.crypt.hashDevice()
        # check if hash of the device exists, if exists no need to make device key
        key = self.getDeviceKey(hashdevice)

        if key is None:

            rsadevice = self.crypt.generateRsa()
            devkey = self.crypt.rsaExport(rsadevice, hashdevice)

            # save key to DB
            # original {"hash" : "ola", "userID" : "1","deviceKey" : "loles"}
            #obj = {"hash": hash, "userID": self.userID, "deviceKey": devkey}

            #obj = {u"hashdevice": u"hash", u"self.userID": u"userID", u"devkey": u"deviceKey"}
            #body = json.dumps(obj)
            #r = requests.post("http://httpbin.org/post", data = {"key":"value"})
            #body = json.dumps({u"body": u"Sounds great! I'll get right on it!"})
            #r = requests.post(api.SAVEDEVICE, data=None,json=body)
            r = requests.post(api.SAVEDEVICE, data={"hash":"hasdevice", "userID": "self.userID", "deviceKey": "devkey"})

            print "Status post: ", r.status_code


    def getDeviceKey(self, hashdevice):

        # with userID and hash get device key

        try:
            result = requests.get(api.GETDEVICE+str(self.userID)+"/"+hashdevice+"/", verify=True)
            if result.status_code == 200:
                res = json.loads(result.text)
                key = res['deviceKey']
                return self.crypt.rsaImport(key, hashdevice)

            # 204 - no content found
            if result.status_code == 204:
                return None

        except requests.ConnectionError:
            print co.FAIL+"Error connecting with server!\n"+co.ENDC
            return

