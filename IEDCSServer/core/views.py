from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

from .models import User, Player
from .forms import registerUserForm


# def index(request):
#     return HttpResponse("Hello, world. You're at the iedcs index.")

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
    template = loader.get_template('core/Account/login.html')
    return HttpResponse(template.render())


def register(request):
    # template = loader.get_template('core/Account/register.html')
    if request.method == 'POST':
        form = registerUserForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)

            ### TODO generate userKey, playerKey and create player in database.
            form.userKey = "aaaaaaaaaaaa"

            form.save()

            return HttpResponseRedirect('../login/')
    else:
        form = registerUserForm()

    return render(request, 'core/Account/register.html', {'form': form})


def manage(request):
    template = loader.get_template('core/Account/manage.html')
    return HttpResponse(template.render())