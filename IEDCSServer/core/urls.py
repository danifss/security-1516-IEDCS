from django.conf.urls import url

from . import views


urlpatterns = [
    # ex: /
    url(r'^$', views.index, name='index'),
    # ex: /about/
    url(r'^about/$', views.about, name='about'),
    # ex: /contact/
    url(r'^contact/$', views.contact, name='contact'),
    # ex: /Account/login/
    url(r'^Account/login/$', views.login, name='login'),
    # ex: /Account/login/
    url(r'^Account/logout/$', views.logout, name='logout'),
    # ex: /Account/register/
    url(r'^Account/register/$', views.register, name='register'),
    # ex: /Account/manage/
    url(r'^Account/manage/$', views.accountManage, name='manage'),
    # ex: /content/
    url(r'^content/$', views.listContent, name='content'),
    # ex: /content/buy/1
    url(r'^content/buy/(?P<pk>[0-9]+)/$', views.buyContent, name='buyContent'),
]
