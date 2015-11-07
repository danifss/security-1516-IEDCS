from Resources import *
import sys
import requests
import json


class Core(object):
    userID = ""
    userName = ""
    email = ""
    firstName = ""
    lastName = ""
    loggedIn = False

    def __init__(self):
        while(not self.loggedIn):
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
            result = requests.get(api.LOGIN+"?username="+username+"&password="+passwd, verify=True)
        except requests.ConnectionError as e:
            print co.FAIL+"Error connecting with server!\n"+co.ENDC
            return;
        if result.status_code == 200:
            res = json.loads(result.text)
            self.userID = res['id']
            self.email = res['email']
            self.firstName = res['first_name']
            self.lastName = res['last_name']
            self.loggedIn = True
        else:
            print co.FAIL+"\tFail doing log in. Error: "+str(result.status_code)+co.ENDC


    ### Logout
    def logout(self):
        self.userID = self.userName = self.email = self.firstName = self.lastName = ""
        self.loggedIn = False
        print co.WARNING + "Logged out with success." + co.ENDC


    ### List content from logged user
    def list_my_content(self):
        try:
            result = requests.get(api.GETCONTENTBYUSER+str(self.userID), verify=True)
            if result.status_code == 200:
                res = json.loads(result.text)

        except requests.ConnectionError as e:
            print co.FAIL+"Error connecting with server!\n"+co.ENDC
            return;
        print co.OKBLUE+"\tThis is your content:"+co.ENDC



    ### Play content bought by the logged client
    def show_my_content(self):
        print "Showing content"
