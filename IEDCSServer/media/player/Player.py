#!/usr/bin/python
from Resources import *
from Core import *
import sys
from webbrowser import open as browser


try:
    ### Initialize core of the system
    core = Core()

    ### Lyfecycle of the program
    while(True):
        print co.BOLD + co.OKBLUE + "\n\n\t\t  Welcome to IEDCS Player"
        print "\tIdentity Enabled Distribution Control System" + co.ENDC
        print co.OKGREEN +"\nOptions:"
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


        ### Handling options
        if op == '1': # login/logout
            # core.show_my_info()
            core.logout() if core.loggedIn else core.login()
        elif op == '2' and core.loggedIn: # personal info
            core.show_my_info()
        elif op == '3' and core.loggedIn: # show my purchases
            core.list_my_content()
        elif op == '4' and core.loggedIn: # play some content
            print co.OKGREEN+co.BOLD
            opt = raw_input("\tWhat do you wanna watch? "+co.ENDC)
            try:
                int_opt = int(opt)
                core.play_my_content(int_opt)
            except Exception as e:
                print co.FAIL+"Invalid option, sorry!"
        elif op == '5' and core.loggedIn: # go to webpage
            browser(api.HOMEPAGE)


        elif op == 'x':
            print co.BOLD + co.HEADER + "Terminated by user! See you soon."+co.ENDC
            sys.exit(0)
        else:
            print co.WARNING + "\nInvalid option, sorry!" + co.ENDC

except KeyboardInterrupt:
    print co.FAIL+"\n\nProgram interrupted by user. Bye!"+co.ENDC
    sys.exit(1)
except Exception as e:
    print co.FAIL+"Oops, unexpected error!\n{0}".format(e)+co.ENDC
    sys.exit(2)

