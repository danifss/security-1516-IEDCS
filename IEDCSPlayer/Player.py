from Resources import *
from Core import *
import sys
from webbrowser import open as browser


try:
    core = Core()

    while(True):
        print co.BOLD + co.OKBLUE + "\n\n\t\t  Welcome to IEDCS Player"
        print "Identity Enabled Distribution Control System" + co.ENDC
        print co.OKGREEN +"\nOptions:"
        if not core.loggedIn:
            print "(1) Log me in"
        else:
            print "(1) Log me out"
            print "(2) Show me my stuff"
            print "(3) Play my stuff"
            print "(4) Buy more stuff"
        print "(x) Say bye to my stuff"
        print "" + co.BOLD
        op = raw_input("Choice: ")
        print co.ENDC



        if op == '1':
            core.logout() if core.loggedIn else core.login()
        elif op == '2' and core.loggedIn:
            core.list_my_content()
        elif op == '3' and core.loggedIn:
            core.show_my_content()
        elif op == '4' and core.loggedIn:
            browser(api.HOMEPAGE)



        elif op == 'x':
            print co.BOLD + co.HEADER + "Terminated by user! See you soon."
            sys.exit(0)
        else:
            print co.WARNING + "\nInvalid option, sorry!" + co.ENDC


except KeyboardInterrupt:
    print co.FAIL+"\n\nProgram interrupted by user. Bye!"
    sys.exit(1)
except Exception as e:
    print co.FAIL+"Oops, unexpected error!\n{0}".format(e)
    sys.exit(2)

