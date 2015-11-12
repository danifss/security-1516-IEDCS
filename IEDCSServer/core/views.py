# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext, loader

from .models import User, Player
from .forms import registerUserForm, AuthenticationForm

from CryptoModule import *

import sys


def index(request):
    # fields = User._meta.get_fields()
    # my_field = User.get #._meta.get_field('firstName')
    # first_name = getattr(User, "firstName")
    # last_name = getattr(User, "lastName")
    template = loader.get_template('core/index.html')
    # context = RequestContext(request, {
    #     'first_name' : my_field,
    # })
    return HttpResponse(template.render())


def about(request):
    template = loader.get_template('core/about.html')
    return HttpResponse(template.render())


def contact(request):
    template = loader.get_template('core/contact.html')
    return HttpResponse(template.render())


def login(request):
    # template = loader.get_template('core/Account/login.html')
    msgError = ''
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = str(form.cleaned_data['username'])
            password = str(form.cleaned_data['password'])

            user = authenticate(username=username, password=password)
            if user is not None:
                # the password verified for the user
                if user:
                    print("User is valid, active and authenticated")
                    return HttpResponseRedirect('../')

                else:
                    print("The User is not valid!")
                    msgError ='The User is not valid!'
            else:
                # the authentication system was unable to verify the username and password
                print("The username and password were incorrect.")
                msgError ='The username and password were incorrect.'
    else:
        form = AuthenticationForm()

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

