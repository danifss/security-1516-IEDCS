#!/usr/bin/python
from Resources import *
from CryptoModuleP import *
import sys, os
import getpass
import requests
import json
import subprocess
import time
import cPickle as pickle
from cStringIO import StringIO
from SmartCard import *
from base64 import b64decode
# from PIL import Image

# import urllib3
# urllib3.disable_warnings()
# import urllib3.contrib.pyopenssl
# urllib3.contrib.pyopenssl.inject_into_urllib3()


class Core(object):
    loggedIn = False

    def __init__(self):
        self.crypt = CryptoModule()
        self.deviceKey = None
        self.playerKey = None
        self.cc_number = 0

        # Check if it is the real user
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
        pteid = SmartCard()
        print co.BOLD + co.OKBLUE + "\n\n\t\t  Logging into IEDCS Player" + co.ENDC
        print co.WARNING
        # every login
        check = pteid.startSession()

        if check:
            print co.FAIL+check+co.ENDC
            self.loggedIn = False
            return

        self.cc_number = pteid.getCCNumber()
        # destroy object to verify later if card was removed
        del pteid

        username = raw_input("\tUsername: ")
        passwd = getpass.getpass('\tPassword:')
        print co.ENDC

        # to try and open player public key
        self.username = username

        self.getPlayerKey()
        passwd_protected = self.crypt.rsaCipher(self.playerKey, passwd)
        url = api.LOGIN+"?username="+username+"&password="+passwd_protected+"&userCC="+self.cc_number

        # url = api.LOGIN+"?username="+username+"&password="+passwd+"&userCC="+self.cc_number

        result = self.request(url)
        if result is None:
            print co.FAIL+"\tFail doing login."+co.ENDC
            return

        if result.status_code == 200:
            ## Load user info
            try:
                f = open('resources/user'+username+'.pkl', 'r')
            except Exception:
                self.loggedIn = False
                print co.FAIL+"\tFail doing login."+co.ENDC
                return

            # get userIV from database
            url = api.GET_USER_IV+str(username)
            result = self.request(url, method="GET")
            if result is None:
                return
            res = json.loads(result.text)
            iv = res["iv"]
            iv_raw = iv.decode('base64')

            decipheredFile = self.crypt.decipherAES('uBAcxUXs1tJYAFSI', iv_raw, f.read())
            f.close()
            src = StringIO(decipheredFile)

            userInfo = pickle.load(src)
            # Import user info
            self.userID = userInfo["userId"]
            self.userCC = userInfo["userCC"]
            self.username = userInfo["username"]
            # agora secalhar nao faz sentido ter aqui a password hashada
            self.password = userInfo["password"]
            self.email = userInfo["email"]
            self.firstName = userInfo["firstName"]
            self.lastName = userInfo["lastName"]
            self.createdOn = userInfo["createdOn"]

            # Validation to check if user.pkl was renamed to some other existent user
            #if hash_pass == self.password and username == self.username:
            if username == self.username:
                # verifies if can open player key pub
                #self.getPlayerKey()
                # if everything ok, lets generate device key or not
                self.deviceKey = self.generateDevice()
                self.loggedIn = True
                return

        self.loggedIn = False
        print co.FAIL+"\tFail doing login."+co.ENDC


    ### Logout
    def logout(self):
        self.userID = self.userCC = self.username = self.password = ""
        self.email = self.firstName = self.lastName = self.createdOn = ""
        self.deviceKey = self.playerKey = None
        self.loggedIn = False
        print co.WARNING + "Logged out with success." + co.ENDC

    def getPlayerKey(self):
        try:
            f = open('resources/player'+self.username+'.pub', 'r')
            playerPublic = f.read()
            f.close()

            # get player IV from database
            url = api.GET_PLAYER_IV + str(self.username)
            result = self.request(url, method="GET")
            if result is None:
                return
            res = json.loads(result.text)
            iv = res["iv"]
            iv_raw = iv.decode('base64')

            player = self.crypt.decipherAES("vp71cNkWdASAPXp4", iv_raw, playerPublic)
            self.playerKey = self.crypt.rsaImport(player)


        except:
            print co.FAIL+"\tFail loading files."+co.ENDC
            os._exit(0)


    ### List content from logged user
    def list_my_content(self):
        url = api.GET_CONTENT_BY_USER + str(self.userID)
        result = self.request(url)
        if result is None:
            return

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



    ### Play content bought by the logged client
    def play_my_content(self):
        hasContent = self.hasContentToPlay()
        if hasContent is None:
            print co.HEADER+co.BOLD+"\tYou need to buy something!"+co.ENDC
            return

        try:
            print co.OKGREEN+co.BOLD
            opt = raw_input("\tWhat do you wanna watch? "+co.ENDC)
            contentID = int(opt)

            # Get pages number to view one by one
            pages = 0
            url = api.GET_CONTENT_PAGES + str(contentID)
            result = self.request(url)
            if result is None:
                return

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
                url = api.GET_CONTENT_TO_PLAY+str(self.userID)+'/'+str(contentID)+'/'+str(i)
                result = self.request(url)
                if result is None:
                    return

                if result.status_code == 200:
                    res = json.loads(result.text)
                    cfname = res['path']

                    # decipher content, dataKey ((f1,f2), dataCiphered)
                    dataKey = self.genFileKey(cfname)
                    if dataKey is None:
                        raise Exception("Don't have permissions to open the file")

                    key = dataKey[0][0]
                    vi = dataKey[0][1]
                    data = dataKey[1].decode('base64')
                    decifrado = self.crypt.decipherAES(key, vi, data)
                    os.remove(cfname)
                    # save to disk
                    filePath = cfname+'.jpg'

                    ## TODO use StringIO to use opencv or something (if we have time)

                    f4 = open(filePath, 'w')
                    f4.write(decifrado)
                    f4.close()

                    try:
                        p = subprocess.Popen(["display", filePath])
                        time.sleep(0.1)
                        os.remove(filePath)
                        while True:
                            opt = raw_input("Next image? (y/n/x) ")
                            if opt == 'y':
                                p.kill()
                                break
                            elif opt == 'x':
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

    def genFileKey(self, cfname):

        if self.playerKey is None or self.deviceKey is None:
            return None

        # 1 step: decipher magic key with devicekey key
        with open(cfname, "r+") as f:
            fileCiphered = f.read()

        header = fileCiphered.split('#')
        magicProtected = header[1]
        magicPlain = self.crypt.rsaDecipher(self.deviceKey, magicProtected)

        # 2 step: cipher magic key with player key Public
        magicSend = self.crypt.rsaCipher(self.playerKey, magicPlain)
        # 3 step: send magicSend to server and receive aux key to start decrypting file
        # api = self.userID, magicSend
        url = api.CHALLENGE
        data = { "userId": str(self.userID), "magicKey": magicSend }
        result = self.request(url, data=data, method='POST')
        if result is None:
            return

        # 3 step: send magicSend to server and receive aux key to start decrypting file
        #result = requests.post(api.CHALLENGE, data={"userId": str(self.userID), "magicKey": magicSend})

        if result.status_code == 200:
            res = json.loads(result.text)
            auxServer = res['challenge']
            fileKey = self.auxFileKey(auxServer)
            return (fileKey,header[2])
        else:
            return None

    def auxFileKey(self,aux):

        if self.playerKey is None or self.deviceKey is None:
            return None

        deviceKeyPub = self.crypt.publicRsa(self.deviceKey)

        pk = CryptoModule.hashingSHA256(str(self.playerKey.exportKey()))
        dk = CryptoModule.hashingSHA256(str(deviceKeyPub))

        xor1 = ""
        for i in range(0, len(pk)):
            xor1 += str(self.logical_function(aux[i], pk[i]))
        hash_xor1 = CryptoModule.hashingSHA256(xor1)

        fileKey = ""
        for i in range(0, len(dk)):
            fileKey += self.logical_function(hash_xor1[i], dk[i])
        fileKey = CryptoModule.hashingSHA256(fileKey)

        p1 = fileKey[8:24]
        p2 = fileKey[37:53]

        return (p1,p2)


    def logical_function(self, str1, str2):
        return str1 + str2

    ### Verify if user has something to Play
    def hasContentToPlay(self):
        url = api.HAS_CONTENT_TO_PLAY+str(self.userID)
        result = self.request(url)
        return result if result is not None else None


    ### Show personal information
    def show_my_info(self):
        print co.HEADER+co.BOLD+"User CC   : "+co.ENDC+ \
              co.OKGREEN+self.userCC+co.ENDC
        print co.HEADER+co.BOLD+"Username  : "+co.ENDC+ \
              co.OKGREEN+self.username+co.ENDC
        print co.HEADER+co.BOLD+"Email     : "+co.ENDC+ \
              co.OKGREEN+self.email+co.ENDC
        print co.HEADER+co.BOLD+"First Name: "+co.ENDC+ \
              co.OKGREEN+self.firstName+co.ENDC
        print co.HEADER+co.BOLD+"Last Name : "+co.ENDC+ \
              co.OKGREEN+self.lastName+co.ENDC
        print co.HEADER+co.BOLD+"Created On: "+co.ENDC+ \
              co.OKGREEN+str(self.createdOn)[:-13]+co.ENDC

    # generates device key if it's the first run
    def generateDevice(self):
        print co.BOLD+"\nChecking Device integrity..."+co.ENDC

        hashdevice = self.crypt.hashDevice()
        # check if hash of the device exists, if exists no need to make device key
        key = self.getDeviceKey()

        if key is None:

            rsadevice = self.crypt.generateRsa()
            devkey = self.crypt.rsaExport(rsadevice, hashdevice)

            devpub = self.crypt.publicRsa(rsadevice)

            # cipher and save key to DB, key = first 16 bits of the hash, vi = more 16bits of the hash
            devsafe = self.crypt.cipherAES(hashdevice[0:16], hashdevice[32:48], devpub)
            f = open('resources/device.priv', 'w')
            f.write(devkey)
            f.close()

            # register new device in DB
            url = api.SAVE_DEVICE
            data = { "hash": hashdevice, "userID": str(self.userID), "deviceKey": devsafe }
            result = self.request(url, data=data, method="POST")
            if result is None:
                return

            if result.status_code == 200:
                print co.HEADER+co.BOLD+"Uouu! Your first time here! Hope you enjoy it.\n"+co.ENDC
            else:
                # if user on the DB doesn't exits, player has to go down
                print "\033[91mDevice Not Valid!!! Player Terminating 1\n\n\033[0m"
                # on second run, the device key would be valid
                os.remove('resources/device.priv')
                # shuts down the player
                os._exit(0)

            return rsadevice
        else:
            print co.OKGREEN+co.BOLD+"Yes, this is not your first time! (Device Validated)\n"+co.ENDC
            return key

    def getDeviceKey(self):
        try:
            f = open('resources/device.priv', 'r')
            key = f.read()
            f.close()

            # always verifies if it's the right device
            hashdevice = self.crypt.hashDevice()

            devkey = self.crypt.rsaImport(key, hashdevice)
            if devkey is None:
                print "\033[91mDevice Not Valid!!! Player Terminating 2\n\n\033[0m"
                os._exit(0)  #shuts down the player
            return devkey
        except:
            return None


    ### Request to server
    def request(self, url, data=None, method="GET"):
        try:
            if method == "GET":
                result = requests.get(url, verify='resources/CA-IEDCS.crt')
            elif method == "POST":
                result = requests.post(url, data=data, verify='resources/CA-IEDCS.crt')
            return result if result.status_code == 200 else None
        except requests.ConnectionError:
            print co.FAIL+"Error connecting with server!\n"+co.ENDC
            return
