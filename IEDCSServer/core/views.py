# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext, loader

from .models import User, Player, Content, Purchase
from .forms import registerUserForm, loginForm

from CryptoModuleS import *

import sys
import os
import cPickle as pickle
from cStringIO import StringIO
import subprocess
import time
import zipfile


def index(request):
    template = loader.get_template('core/index.html')
    loggedIn = False
    if 'firstName' in request.session and 'loggedIn' in request.session:
        firstName = request.session['firstName']
        loggedIn = request.session['loggedIn']
    else:
        firstName = "Visitante"
        request.session['firstName'] = firstName
        request.session['loggedIn'] = False

    context = RequestContext(request, {
        'firstName' : firstName,
        'loggedIn' : loggedIn,
    })
    return HttpResponse(template.render(context))


def about(request):
    if 'loggedIn' not in request.session or request.session['loggedIn'] == False or 'username' not in request.session:
        request.session['firstName'] = "Visitante"
        request.session['loggedIn'] = False

    template = loader.get_template('core/about.html')
    return HttpResponse(template.render({'loggedIn' : request.session['loggedIn'], 'firstName' : request.session['firstName']}))


def contact(request):
    if 'loggedIn' not in request.session or request.session['loggedIn'] == False or 'username' not in request.session:
        request.session['firstName'] = "Visitante"
        request.session['loggedIn'] = False

    template = loader.get_template('core/contact.html')
    return HttpResponse(template.render({'loggedIn' : request.session['loggedIn'], 'firstName' : request.session['firstName']}))


def login(request):
    if 'loggedIn' not in request.session or request.session['loggedIn'] == False or 'username' not in request.session:
        request.session['firstName'] = "Visitante"
        request.session['loggedIn'] = False

    msgError = ''
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid:
            username = str(request.POST['username']) # str(form.cleaned_data['username'])
            password = str(request.POST['password']) # str(form.cleaned_data['password'])

            user = authenticate(username=username, password=password)
            if user is not None:
                # get user and set session
                if user:
                    try:
                        utilizador = User.objects.get(username=username)
                        request.session['firstName'] = str(utilizador.firstName)
                        request.session['username'] = str(utilizador.username)
                        request.session['loggedIn'] = True
                    except Exception as e:
                        print "Some error acurred getting user to logging in.", e
                        request.session['firstName'] = "Visitante"
                        request.session['loggedIn'] = False
                        return HttpResponseRedirect('/Account/login/')
                    return HttpResponseRedirect('/')
                else:
                    print "The User is not valid!"
                    request.session['firstName'] = "Visitante"
                    request.session['loggedIn'] = False
                    msgError ='The User is not valid!'
            else:
                # the authentication system was unable to verify the username and password
                print "The username and password were incorrect."
                request.session['firstName'] = "Visitante"
                request.session['loggedIn'] = False
                msgError ='The username and password were incorrect.'
    else:
        form = loginForm()

    request.session['firstName'] = "Visitante"
    request.session['loggedIn'] = False
    context = RequestContext(request, {
        'error_message' : msgError,
    })
    return render(request, 'core/Account/login.html', {'form': form, \
                   'loggedIn' : request.session['loggedIn'], 'firstName' : request.session['firstName']})

def authenticate(username, password):
    try:
        # validate if username exists
        user = User.objects.get(username=username)
    except:
        print "Error getting user by username!"
        return None
    # validate password
    crypt = CryptoModule()
    sha_pass = crypt.hashingSHA256(password)
    bd_pass = user.password
    if bd_pass != sha_pass:
        return False
    # all good
    return True


def logout(request):
    request.session['firstName'] = "Visitante"
    request.session['loggedIn'] = False
    template = loader.get_template('core/Account/logout.html')
    return HttpResponse(template.render({'loggedIn' : request.session['loggedIn'], 'firstName' : request.session['firstName']}))


@csrf_protect
def register(request):
    if 'loggedIn' not in request.session or request.session['loggedIn'] == False or 'username' not in request.session:
        request.session['firstName'] = "Visitante"
        request.session['loggedIn'] = False

    if request.method == 'POST':
        form = registerUserForm(request.POST)
        if form.is_valid():
            # instantiate Crypto Module
            crypt = CryptoModule()

            ### Get form data
            email = str(form.cleaned_data['email'])
            password = str(form.cleaned_data['password'])
            username = str(form.cleaned_data['username'])
            firstName = str(form.cleaned_data['lastName'])
            lastName = str(form.cleaned_data['firstName'])

            # save form without commit changes
            form = form.save(commit=False)

            # apply SHA256 to password
            form.password = crypt.hashingSHA256(password)

            # Generate symmetric userKey with AES with user details
            uk = email+username+lastName+password+firstName
            userkeyHash = crypt.hashingSHA256(uk)

            # userkeyHash[0:16], userkeyHash[48:64]
            # just a decoy, the user key is the hash
            userkeyString = crypt.cipherAES("uBAcxUXs1tJY/FSI", "vp71cNkWd/SAPXp4", userkeyHash)

            form.userKey = userkeyString

            # effectively registers new user in db
            form.save()

            # Create new Player with associated playerKey
            pk = email[:len(email)/2]+password[len(password)/2:]+username
            playerHash = crypt.hashingSHA256(pk)
            playerRsa = crypt.generateRsa()

            # save to file, ciphered
            playerPublic = playerRsa.publickey().exportKey("PEM")
            playerPublicSafe = crypt.cipherAES("AF9dNEVWEG7p6A9m", "o5mgrwCZ0FCbCkun", playerPublic)

            # write public key into file
            f = open(settings.MEDIA_ROOT+'/tmp/resources/player'+username+'.pub', 'w')
            f.write(playerPublicSafe)
            f.close()

            # passphrase playerHash
            playerKey = crypt.rsaExport(playerRsa, playerHash)

            user = User.objects.get(username=username)
            try:
                new_player = Player(playerKey=playerKey, user=user)

            except :
                print "Error getting creating new Player."
                return HttpResponseRedirect('../register/')

            # Save new Player in DB
            new_player.save()

            ### Write static data to specific user
            writeUserData(user)
            ### Create Player file to download
            createDownloadFile(user.userID, user.username)

            return HttpResponseRedirect('../login/')
    else:
        form = registerUserForm()

    return render(request, 'core/Account/register.html', {'form': form, \
                  'loggedIn' : request.session['loggedIn'], 'firstName' : request.session['firstName']})

# Function to write personal data of user into file and then cipher the file
def writeUserData(user=None):
    if user is None:
        print 'Error writing User data - No User'
        return
    # create user info dictionary
    userInfo = {}
    userInfo["userId"] = user.userID
    userInfo["username"] = user.username
    userInfo["password"] = user.password
    userInfo["email"] = user.email
    userInfo["firstName"] = user.firstName
    userInfo["lastName"] = user.lastName
    userInfo["createdOn"] = user.createdOn
    # buffer for pickle dump
    src = StringIO()
    # pickle data to string io
    pickle.dump(userInfo, src)
    # cipher file
    crypt = CryptoModule()
    c = crypt.cipherAES('1chavinhapotente','umVIsupercaragos', src.getvalue())
    # open file to write ciphered pickled object
    f = open('media/tmp/resources/user'+user.username+'.pkl', 'w')
    f.write(c)
    f.close()

# Function to create zip file to be downaloaded by a specific user
### http://nuitka.net/doc/user-manual.html#use-case-1-program-compilation-with-all-modules-embedded
def createDownloadFile(userID, username):
    # execute nuitka
    # command = "--recurse-all --recurse-directory=media/player/resources/ --output-dir=media/player/ --remove-output media/player/Player.py"
    """
    options = ["--recurse-all", "--output-dir=media/tmp/", "--recurse-directory=media/player/resources/", \
               "--remove-output", "media/player/Player.py"]
    p = subprocess.Popen(["nuitka"]+options)
    # Wait for the command to finish
    p.wait()
    """
    # Making zip file to be downloaded
    ### TODO move files in player/resources folder to zip file
    filenames = ['media/download/Player.exe', 'media/player/resources',
                    'media/player/resources/player'+username+'.pub',
                    'media/player/resources/user'+username+'.pkl']
    # zip names
    zip_subdir = 'download'+str(userID)
    zip_filename = "%s.zip" % zip_subdir
    zip_path = 'media/tmp/'

    # zip compressor
    try:
        zf = zipfile.ZipFile('media/download/'+zip_filename, "w")
        for root, dirs, files in os.walk(zip_path):
            for file in files:
                zf.write(os.path.join(root, file))
                # for fpath in filenames:
                # Calculate path for file in zip
                # fdir, fname = os.path.split(fpath)
                # print fdir, fname
                # zip_path = os.path.join('IEDCSPlayer', fname)
                # Add file, at correct path
                # zf.write(fpath, zip_path)
        zf.close()
        # clean files
        os.remove('media/tmp/resources/player'+username+'.pub')
        os.remove('media/tmp/resources/user'+username+'.pkl')
        # os.remove('media/download/Player.exe')
    except Exception as e:
        print "ERROR ", e


def accountManage(request):
    if 'loggedIn' not in request.session or request.session['loggedIn'] == False or 'username' not in request.session:
        request.session['firstName'] = "Visitante"
        request.session['loggedIn'] = False
        template = loader.get_template('core/index.html')
        return HttpResponse(template.render({'loggedIn' : request.session['loggedIn']}))

    try:
        user = User.objects.get(username=request.session['username'])
        playerUrl = 'media/download/download'+str(user.userID)+'.zip' # settings.MEDIA_URL
        if not os.path.isfile(playerUrl):
            playerUrl = '#'

        context = RequestContext(request, {
            'username' : user.username,
            'email' : user.email,
            'firstName' : user.firstName,
            'lastName' : user.lastName,
            'createdOn' : user.createdOn,
            'playerUrl' : playerUrl,
            'loggedIn' : request.session['loggedIn'],
        })

    except Exception as e:
        print "Error getting User details.", e
        return HttpResponseRedirect('/')

    template = loader.get_template('core/Account/manage.html')
    return HttpResponse(template.render(context))


def listContent(request):
    if 'loggedIn' not in request.session or request.session['loggedIn'] == False or 'username' not in request.session:
        request.session['firstName'] = "Visitante"
        request.session['loggedIn'] = False
        template = loader.get_template('core/index.html')
        return HttpResponse(template.render({'loggedIn' : request.session['loggedIn'], \
                             'firstName' : request.session['firstName']}))

    try:
        content = Content.objects.all()
        context = RequestContext(request, {
            'content' : content,
            'loggedIn' : request.session['loggedIn'],
            'firstName' : request.session['firstName'],
        })
    except Exception as e:
        print "Error getting Content.", e
        return HttpResponseRedirect('/')

    template = loader.get_template('core/content.html')
    return HttpResponse(template.render(context))


def buyContent(request, pk=None):
    if 'loggedIn' not in request.session or request.session['loggedIn'] == False or 'username' not in request.session:
        request.session['firstName'] = "Visitante"
        request.session['loggedIn'] = False
        template = loader.get_template('core/index.html')
        return HttpResponse(template.render({'loggedIn' : request.session['loggedIn'], \
                             'firstName' : request.session['firstName']}))

    result = False
    try:
        user = User.objects.get(username=request.session['username'])
        print user.userID
        content = Content.objects.get(contentID=pk)
        print content.contentID
        new_purchase = Purchase(content=content, user=user)
        new_purchase.save()
        result = True
        context = RequestContext(request, {
            'result' : result,
            'loggedIn' : request.session['loggedIn']
        })
    except Exception as e:
        print "Error making purchase action.", e
        return HttpResponseRedirect('/')

    template = loader.get_template('core/purchase_content.html')
    return HttpResponse(template.render(context))
