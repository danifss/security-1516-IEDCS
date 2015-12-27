#!/usr/bin/python
from Resources import *
from Core import *
import sys
from webbrowser import open as browser
from SmartCard import *

try:
    ### Initialize core of the system
    core = Core()

    #smart.startSession()


    ### Lyfecycle of the program
    while True:


        print co.BOLD + co.OKBLUE + "\n\n\t\t  Welcome to IEDCS Player"
        print "\tIdentity Enabled Distribution Control System" + co.ENDC
        print co.OKGREEN + "\nOptions:"
        if not core.loggedIn:
            print "(1) Log me in"
        else:
            print "(1) Log me out"
            print "(2) My personal information"
            print "(3) Show me my stuff"
            print "(4) Play my stuff"
            print "(5) Buy more stuff"
        print "(x) Say bye to my stuff"
        print "" + co.BOLD
        op = raw_input("Choice: ")
        print co.ENDC

        # verifies if the smartcard or reader was removed and if it's still the same smartcard
        smart = SmartCard()
        check = smart.startSession()
        if check:
            print co.FAIL+"Program interrupted by user: "+check+co.ENDC
            sys.exit(3)
        if core.cc_number != smart.getCCNumber():
            print co.FAIL+"Program interrupted by user: don't exchange smartcards!"+co.ENDC
            sys.exit(3)

        # destroy object to verify later if card was removed
        del smart

        ### Handling options
        if op == '1':  # login/logout
            core.logout() if core.loggedIn else core.login()

        elif op == '2' and core.loggedIn:  # personal info
            core.show_my_info()
        elif op == '3' and core.loggedIn:  # show my purchases
            core.list_my_content()
        elif op == '4' and core.loggedIn:  # play some content
            core.play_my_content()
        elif op == '5' and core.loggedIn:  # go to webpage
            browser(api.HOMEPAGE)


        elif op == 'x':
            print co.BOLD + co.HEADER + "Terminated by user! See you soon." + co.ENDC
            sys.exit(0)
        else:
            print co.WARNING + "\nInvalid option, sorry!" + co.ENDC

except KeyboardInterrupt:
    print co.FAIL + "\n\nProgram interrupted by user. Bye!" + co.ENDC
    sys.exit(1)
except Exception as e:
    print co.FAIL + "Oops, unexpected error!\n{0}".format(e) + co.ENDC
    sys.exit(2)
