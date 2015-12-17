#!/usr/bin/python
from Resources import *
from CryptoModule import *
import sys, os
import getpass
import requests
import json
import subprocess
import time
import pickle
from cStringIO import StringIO
# from PIL import Image


class Core(object):
    # userID = ""
    # username = ""
    # password = ""
    # email = ""
    # firstName = ""
    # lastName = ""
    # createdOn = ""
    loggedIn = False


    def __init__(self):

        self.crypt = CryptoModule()

        # Check if it is the real user
        while not self.loggedIn:
            # user mut be logged in
            self.login()
            if not self.loggedIn:
                op = raw_input("\tExit?(y/N) ")
                if op == 'y':
                    print co.BOLD + co.HEADER + "\nTerminated by user! See you soon.\n"
                    sys.exit(0)

        f = open('resources/player'+self.username+'.pub', 'r')
        playerPublic = f.read()
        f.close()
        player = self.crypt.decipherAES("AF9dNEVWEG7p6A9m", "o5mgrwCZ0FCbCkun", playerPublic)
        self.playerHash = self.crypt.hashingSHA256(player)
        # self.playerKey = self.crypt.rsaImport(player)

        ### print welcome message
        print co.HEADER+"\tWelcome "+co.BOLD+self.firstName+" "+self.lastName+co.ENDC


    ### Login
    def login(self):
        print co.BOLD + co.OKBLUE + "\n\n\t\t  Logging into IEDCS Player" + co.ENDC
        print co.WARNING
        username = raw_input("\tUsername: ")
        passwd = getpass.getpass('\tPassword:')
        print co.ENDC

        ## Load user info
        f = open('resources/user.pkl', 'rb')
        decipheredFile = self.crypt.decipherAES('1chavinhapotente','umVIsupercaragos',f.read())
        f.close()
        fileInMem = StringIO(decipheredFile)
        userInfo = pickle.Unpickler(fileInMem)
        # Import user info
        self.userID = userInfo.userID
        self.username = userInfo.username
        self.password = userInfo.password
        self.email = userInfo.email
        self.firstName = userInfo.firstName
        self.lastName = userInfo.lastName
        self.createdOn = userInfo.createdOn

        try:
            hash_pass = self.crypt.hashingSHA256(passwd)
            # result = requests.get(api.LOGIN+"?username="+username+"&password="+hash_pass, verify=True)
            nice_try = True if hash_pass == self.password else False
        except requests.ConnectionError:
            print co.FAIL+"Error connecting with server!\n"+co.ENDC
            return
        # if result.status_code == 200:
        if nice_try:
            # res = json.loads(result.text)
            # self.username = username
            # self.userID = res['id']
            # self.email = res['email']
            # self.firstName = res['first_name']
            # self.lastName = res['last_name']
            self.loggedIn = True

            # if everything ok, lets generate device key or not
            self.deviceKey = self.generateDevice()
        else:
            print co.FAIL+"\tFail doing login."+co.ENDC #+str(result.status_code)+co.ENDC


    ### Logout
    def logout(self):
        self.userID = self.username = self.password = self.email = self.firstName = self.lastName = self.createdOn =  ""
        self.deviceKey = self.playerHash = ""
        self.crypt = None
        self.loggedIn = False
        print co.WARNING + "Logged out with success." + co.ENDC


    ### List content from logged user
    def list_my_content(self):
        try:
            result = requests.get(api.GET_CONTENT_BY_USER + str(self.userID), verify=True)
            if result.status_code == 200:
                res = json.loads(result.text)['results']
                if len(res) > 0:
                    print co.OKBLUE+co.BOLD+"\tThis is your content:\n"+co.ENDC
                    print co.HEADER+co.BOLD+"  ID  \t   Date of purchase\t\t    Name of product"+co.ENDC
                    distinct = []
                    for item in res:
                        if item not in distinct:
                            distinct += [item]
                            print co.OKGREEN+"  "+str(item['contentID'])+"\t"+item['createdOn']+"\t    "+item['name']+co.ENDC
                else:
                    print co.HEADER+co.BOLD+"\tYou need to buy something!"+co.ENDC

        except requests.ConnectionError:
            print co.FAIL+"Error connecting with server!\n"+co.ENDC
            return


    ### Play content bought by the logged client
    def play_my_content(self, contentID):
        try:
            # Get pages number to view one by one
            pages = 0
            result = requests.get(api.GET_CONTENT_PAGES + str(contentID), verify=True)
            if result.status_code == 200:
                res = json.loads(result.text)
                pages = int(res['pages'])
            else:
                print co.FAIL+"Invalid content number. Please choose one from your bought list."+co.ENDC
                return

            print co.OKBLUE+co.BOLD+"\nPlaying content "+co.WARNING+"#"+str(contentID)+co.ENDC
            i = 0
            while i <= pages:
                i += 1
                result = requests.get(api.GET_CONTENT_TO_PLAY+str(self.userID)+'/'+str(contentID)+'/'+str(i))
                if result.status_code == 200:
                    res = json.loads(result.text)
                    cfname = res['path']

                    # decipher content
                    fileKey = self.genFileKey()
                    f1 = open(cfname, 'r')
                    decifrado = self.crypt.decipherAES(fileKey[0], fileKey[1], f1.read())
                    f1.close()
                    os.remove(cfname)
                    # save to disk
                    filePath = cfname+'.jpg'
                    # TODO use cStringIO to do everything in memory
                    f4 = open(filePath, 'w')
                    f4.write(decifrado)
                    f4.close()

                    try:
                        p = subprocess.Popen(["display", filePath])
                        time.sleep(0.3)
                        os.remove(filePath)
                        while True:
                            opt = raw_input("Next image? (y/n/x) ")
                            if opt=='y':
                                p.kill()
                                break
                            elif opt=='x':
                                i = pages + 1
                                p.kill()
                                break
                    except:
                        print co.FAIL+"Something happened opening the file #" + str(i) + co.ENDC
                    # os.remove(filePath)
                else:
                    return co.FAIL+"Error occurred!! "+co.ENDC
        except Exception as e:
            print co.FAIL+"Error occurred!! ", e
            print co.ENDC

    def genFileKey(self):
        return ("+bananasbananas+","+bananasbananas+")


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
        print co.HEADER+co.BOLD+"Created On: "+co.ENDC+ \
              co.OKGREEN+self.createdOn+co.ENDC


    # generates device key if first run
    def generateDevice(self):
        print co.BOLD+"\nChecking Device integrity..."+co.ENDC

        hashdevice = self.crypt.hashDevice()
        # check if hash of the device exists, if exists no need to make device key
        key = self.getDeviceKey(hashdevice)
        if key is None:

            rsadevice = self.crypt.generateRsa()
            devkey = self.crypt.rsaExport(rsadevice, hashdevice)

            devpub = self.crypt.publicRsa(rsadevice)


            # cipher and save key to DB, key = first 16 bits of the hash, vi = more 16bits of the hash
            devsafe = self.crypt.cipherAES(hashdevice[0:16], hashdevice[32:48], devpub)
            f = open('device.priv', 'w')
            f.write(devsafe)
            f.close()

            r = requests.post(api.SAVE_DEVICE, data={"hash":hashdevice, "userID": self.userID, "deviceKey": devsafe})

            # print "Status post: ", r.status_code
            print co.HEADER+co.BOLD+"Uouu! Your first time here! Hope you enjoy it.\n"+co.ENDC
        else:
            print co.OKGREEN+co.BOLD+"Yes, this is not your first time! (Device Validated)\n"+co.ENDC


    def getDeviceKey(self, hashdevice):

        try:
            f = open('device.priv', 'r')
            key = f.read()
            f.close()

            hashdevice = self.crypt.hashDevice()
            devsafe = self.crypt.decipherAES(hashdevice[0:16], hashdevice[32:48], key)
            devkey = self.crypt.rsaImport(devsafe, hashdevice)

            if devkey is None:
                print "\033[91mDevice Not Valid!!! Player Terminating\n\n\033[0m"
                os._exit(0)
            return devkey
        except:
            return None

    # GET DEVICE KEY TO SERVER
    """
    def getDeviceKey(self, hashdevice):

        # with userID and hash get device key
        try:
            result = requests.get(api.GET_DEVICE + str(self.userID) + "/" + hashdevice, verify=True)
            # print result.text
            if result.status_code == 200:
                # print result.text
                res = json.loads(result.text)
                dados = res['results']
                key_ciphered = dados[0]['deviceKey']
                print dados
                hashdevice = self.crypt.hashDevice()
                key = self.crypt.decipherAES(hashdevice[0:16], hashdevice[32:48], key_ciphered)
                return self.crypt.rsaImport(key, hashdevice)

            # 204 - no content found
            if result.status_code == 204:
                return None

        except requests.ConnectionError:
            print co.FAIL+"Error connecting with server!\n"+co.ENDC
            return None
        except Exception as e:
            print co.FAIL+"ERROR!", e
            print co.ENDC
            return None
        """""


