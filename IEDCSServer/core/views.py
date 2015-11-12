# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext, loader

from .models import User, Player
from .forms import registerUserForm, loginForm

from CryptoModule import *

import sys


def index(request):
    # fields = User._meta.get_fields()
    # my_field = User.get #._meta.get_field('firstName')
    # first_name = getattr(User, "firstName")
    # last_name = getattr(User, "lastName")
    template = loader.get_template('core/index.html')
    loggedIn = False
    if 'username' in request.session and 'loggedIn' in request.session:
        firstName = request.session['username']
        loggedIn = request.session['loggedIn']
    else:
        firstName = "Visitante"
        request.session['username'] = firstName
        request.session['loggedIn'] = False

    context = RequestContext(request, {
        'firstName' : firstName,
        'loggedIn' : loggedIn,
    })
    return HttpResponse(template.render(context))


def about(request):
    template = loader.get_template('core/about.html')
    return HttpResponse(template.render())


def contact(request):
    template = loader.get_template('core/contact.html')
    return HttpResponse(template.render())


def login(request):
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
                        request.session['username'] = str(utilizador.firstName)
                        request.session['loggedIn'] = True
                    except Exception as e:
                        print "Some error acurred getting user to logging in.", e
                        request.session.flush()
                        return HttpResponseRedirect('/Account/login/')
                    return HttpResponseRedirect('/')
                else:
                    print "The User is not valid!"
                    request.session.flush()
                    msgError ='The User is not valid!'
            else:
                # the authentication system was unable to verify the username and password
                print "The username and password were incorrect."
                request.session.flush()
                msgError ='The username and password were incorrect.'
    else:
        form = loginForm()

    context = RequestContext(request, {
        'error_message' : msgError,
    })
    return render(request, 'core/Account/login.html', {'form': form})

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
    template = loader.get_template('core/Account/logout.html')
    return HttpResponse(template.render())


@csrf_protect
def register(request):
    # template = loader.get_template('core/Account/register.html')
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
            uk = email[:len(email)/2]+username+lastName[len(lastName)/2:]+password[len(password)/2:]+firstName[len(firstName)/2:]
            userkeyString = crypt.hashingSHA256(uk) ### TODO OR NOT!!! Change this to something ciphered with AES, a key and vi
            form.userKey = userkeyString

            # effectively registers new user in db
            form.save()

            # Create new Player with associated playerKey
            pk = email[:len(email)/2]+password[len(password)/2:]+username
            playerKey = crypt.hashingSHA256(pk) # TODO change to pair of keys
            try:
                new_player = Player(playerKey=playerKey, userId=User.objects.get(username=username))
            except:
                print "Error getting the new register user."
                return HttpResponseRedirect('../register/')

            # Save new Player in DB
            new_player.save()

            ### TODO create Player file to download
            # maybe this is only done when the user makes download of program from webpage

            return HttpResponseRedirect('../login/')
    else:
        form = registerUserForm()

    return render(request, 'core/Account/register.html', {'form': form})


def manage(request):
    template = loader.get_template('core/Account/manage.html')
    return HttpResponse(template.render())


def listContent(request):
    template = loader.get_template('core/content.html')
    return HttpResponse(template.render())

