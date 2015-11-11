from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

from .models import User, Player
from .forms import registerUserForm, AuthenticationForm

from CryptoModule import *



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
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)

        user = authenticate(username='john', password='secret')
        if user is not None:
            # the password verified for the user
            if user.is_active:
                print("User is valid, active and authenticated")
            else:
                print("The password is valid, but the account has been disabled!")
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")
    else:
        form = AuthenticationForm()

    return render(request, 'core/Account/login.html', {'form': form})


def register(request):
    # template = loader.get_template('core/Account/register.html')
    if request.method == 'POST':
        form = registerUserForm(request.POST)
        if form.is_valid():
            # instantiate Crypto Module
            crypt = CryptoModule()

            print form.cleaned_data

            # apply SHA256 to password
            form.password = crypt.hashingSHA256(form.cleaned_data['password'])

            # get email
            email = form.cleaned_data['email']

            # save form without commit changes
            form = form.save(commit=False)

            ### TODO generate userKey, playerKey and create player in database.

            # Generate pair of userKey
            form.userKey = "ddddd"

            form.save()

            # Create new Player with associated playerKey
            playerKey = "swagger"
            new_player = Player(playerKey=playerKey, userId=User.objects.get(email=email))
            new_player.save()

            print new_player.playerID
            form.playerId = new_player.playerID

            return HttpResponseRedirect('../login/')
    else:
        form = registerUserForm()

    return render(request, 'core/Account/register.html', {'form': form})


@login_required
def manage(request):
    template = loader.get_template('core/Account/manage.html')
    return HttpResponse(template.render())


def listContent(request):
    template = loader.get_template('core/content.html')
    return HttpResponse(template.render())

