from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import User


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
    template = loader.get_template('core/Account/register.html')
    return HttpResponse(template.render())


def manage(request):
    template = loader.get_template('core/Account/manage.html')
    return HttpResponse(template.render())