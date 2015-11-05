from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /iedcs/
    url(r'^$', views.index, name='index'),
    # ex: /iedcs/about/
    url(r'^about/$', views.about, name='about'),
    # ex: /iedcs/contact/
    url(r'^contact/$', views.contact, name='contact'),
    # ex: /iedcs/Account/login/
    url(r'^Account/login/$', views.login, name='login'),
    # ex: /iedcs/Account/login/
    url(r'^Account/register/$', views.register, name='register'),
    # ex: /iedcs/Account/manage/
    url(r'^Account/manage/$', views.manage, name='manage'),

]
