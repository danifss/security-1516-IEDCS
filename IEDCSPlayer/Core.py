#!/usr/bin/python
from Resources import *
from CryptoModule import *
import sys, os
import requests
import json
import subprocess


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

        f = open('player.pub', 'r')
        playerPublic = f.read()
        player = self.crypt.decipherAES("AF9dNEVWEG7p6A9m", "o5mgrwCZ0FCbCkun", playerPublic)

        self.crypt

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
        print co.OKBLUE+co.BOLD+"\nPlaying content #"+co.ENDC+str(contentID)

        try:
            # Get pages number to view one by one
            pages = 0
            result = requests.get(api.GET_CONTENT_PAGES + str(contentID), verify=True)
            if result.status_code == 200:
                res = json.loads(result.text)
                pages = int(res['pages'])
            # # Get file name by content id
            # file_name = ""
            # result = requests.get(api.GET_CONTENT_FILENAME + str(contentID), verify=True)
            # if result.status_code == 200:
            #     res = json.loads(result.text)
            #     file_name = res['file_name']
            # # Get file path by content id
            # file_path = ""
            # result = requests.get(api.GET_CONTENT_FILEPATH + str(contentID), verify=True)
            # if result.status_code == 200:
            #     res = json.loads(result.text)
            #     file_path = res['file_path']

            ### TODO decipher the content
            f3 = open('/home/silva/security2015-p2g5/Storage/ghosts/cifrado_'+content.fileName+pg, 'r')
            decifrado = crypto.decipherAES(fileKey[0], fileKey[1], f3.read())
            f3.close()

            f4 = open('/home/silva/security2015-p2g5/Storage/ghosts/decifrado_'+content.fileName+pg, 'w')
            f4.write(decifrado)
            f4.close()
            filePath = "deciphered file path here"

            for i in range(1, pages):
                result = requests.get(api.GET_CONTENT_TO_PLAY+str(self.userID)+'/'+str(contentID)+'/'+str(i))
                print result
                if result.status_code == 200:
                    try:
                        p = subprocess.Popen(["display", "../"+filePath])
                        while True:
                            opt = raw_input("Close image? (y/n) ")
                            if opt=='y':
                                break
                        p.kill()
                    except:
                        print co.FAIL+"Something happened opening the file #" + file_name + str(i) + co.ENDC
                        p.kill()
        except Exception as e:
            print co.FAIL+"Error occurred!! ", e
            print co.ENDC


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
        print co.BOLD+"\nChecking Device integrity..."+co.ENDC

        hashdevice = self.crypt.hashDevice()
        # check if hash of the device exists, if exists no need to make device key
        key = self.getDeviceKey(hashdevice)

        if key is None:

            rsadevice = self.crypt.generateRsa()
            devkey = self.crypt.rsaExport(rsadevice, hashdevice)

            # cipher and save key to DB, key = first 16 bits of the hash, vi = more 16bits of the hash
            devsafe = self.crypt.cipherAES(hashdevice[0:16], hashdevice[32:48], devkey)
            r = requests.post(api.SAVE_DEVICE, data={"hash":hashdevice, "userID": self.userID, "deviceKey": devsafe})

            # print "Status post: ", r.status_code
            print co.HEADER+co.BOLD+"Uouu! Your first time here! Hope you enjoy it.\n"+co.ENDC
        else:
            print co.OKGREEN+co.BOLD+"Yes, this is not your first time!\n"+co.ENDC


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



# c = Core()
# c.play_my_content(1)
