from django.conf.urls import include, url
from api import views


urlpatterns = [

    url(r'^docs/', include('rest_framework_swagger.urls')),

    ### USER
    # ex: /api/user/login/?username=daniel?password=9r3hf83h8gh39g
    url(r'^user/login/$', views.UserLogin.as_view()),
    # ex: /api/user/iv/daniel
    url(r'^user/iv/(?P<un>[\-%_&a-zA-Z0-9]+)$', views.GET_userIV.as_view()),
    ### PLAYER
    # ex: /api/player/iv/2
    url(r'^player/iv/(?P<pk>[0-9]+)$', views.GET_playerIV.as_view()),
    ### DEVICE
    # ex: /api/device/ with JSON attach
    url(r'^device/new/$', views.UserDeviceCreate.as_view()),
    # ex: /api/device/1/j82hf8724hf287f
    url(r'^device/(?P<pk>[0-9]+)/(?P<hash>[a-zA-Z0-9]+)$', views.UserDevice.as_view()),
    ### CONTENT
    # ex: /api/content/user/3
    url(r'^content/user/(?P<pk>[0-9]+)$', views.ContentByUser.as_view()),
    # ex: /api/content/hascontent/2
    url(r'^content/hascontent/(?P<pk>[0-9]+)$', views.UserHasContent.as_view()),
    # ex: /api/content/pages/1
    url(r'^content/pages/(?P<pk>[0-9]+)$', views.ContentPages.as_view()),
    # ex: /api/content/play/1/1/1
    url(r'^content/play/(?P<pk>[0-9]+)/(?P<ct>[0-9]+)/(?P<pg>[0-9]+)$', views.PlayContent.as_view()),
    # ex: /api/content/challenge/ with JSON attach
    url(r'^content/challenge/$', views.ChallengeKey.as_view()),

]
