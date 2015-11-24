# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext, loader

from .models import User, Player, Content, Purchase
from .forms import registerUserForm, loginForm

from CryptoModule import *

import sys
import os
import zipfile
import StringIO


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

            # Generate symmetric userKey with AES from user details
            # uk = email[:len(email)/2]+username+lastName[len(lastName)/2:]+password[len(password)/2:]+firstName[len(firstName)/2:]
            uk = email+username+lastName+password+firstName
            userkeyHash = crypt.hashingSHA256(uk)

            # userkeyHash[0:16], userkeyHash[48:64]
            # just a decoy, the user key is the hash
            userkeyString = crypt.cipherAES(userkeyHash[0:16], userkeyHash[48:64], "bananas")

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

            f = open(settings.MEDIA_ROOT+'/player_keys/player'+username+'.pub', 'w')
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

            ### Create Player file to download
            createDownloadZip(user.userID, user.username)

            return HttpResponseRedirect('../login/')
    else:
        form = registerUserForm()

    return render(request, 'core/Account/register.html', {'form': form, \
                  'loggedIn' : request.session['loggedIn'], 'firstName' : request.session['firstName']})

# Function to create zip file to be downaloaded by a specific user
def createDownloadZip(userID, username):
    # files to zip
    base = 'media/player_keys/'
    # playerDir = base+'IEDCSPlayer/'
    filenames = [base+'player'+username+'.pub', base+'Core.py', base+'CryptoModule.py', \
                 base+'Fingerprint.py', base+'Player.py', base+'Resources.py']
    # zip name
    zip_subdir = 'download'+str(userID)
    zip_filename = "%s.zip" % zip_subdir

    # The zip compressor
    try:
        zf = zipfile.ZipFile('media/player_keys/'+zip_filename, "w")
        for fpath in filenames:
            # Calculate path for file in zip
            fdir, fname = os.path.split(fpath)
            # print fdir, fname
            zip_path = os.path.join('IEDCSPlayer', fname)
            # Add file, at correct path
            zf.write(fpath, zip_path)

        zf.close()
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
        playerUrl = 'media/player_keys/download'+str(user.userID)+'.zip' # settings.MEDIA_URL
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
        return HttpResponse(template.render({'loggedIn' : request.session['loggedIn'], 'firstName' : request.session['firstName']}))

    try:
        content = Content.objects.all()
        context = RequestContext(request, {
            'content' : content,
            'loggedIn' : request.session['loggedIn'],
            'firstName' : request.session['fisrtName'],
        })
    except Exception as e:
        print "Error getting Content.", e
        return HttpResponseRedirect('/')

    template = loader.get_template('core/content.html')
    return HttpResponse(template.render(context))


def buyContent(request, pk=None):
    if 'loggedIn' not in request.session or request.session['loggedIn'] == False:
        request.session['loggedIn'] = False
        template = loader.get_template('core/index.html')
        return HttpResponse(template.render({'loggedIn' : request.session['loggedIn']}))

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
