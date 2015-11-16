from django.conf.urls import include, url
from api import views


urlpatterns = [

    url(r'^docs/', include('rest_framework_swagger.urls')),

    ### USER
    # ex: /api/user/login/?username=daniel?password=9r3hf83h8gh39g
    url(r'^user/login/$', views.UserLogin.as_view()),
    ### DEVICE
    # ex: /api/device/ with JSON attach
    url(r'^device/new/$', views.UserDeviceCreate.as_view()),
    # ex: /api/device/1/j82hf8724hf287f
    url(r'^device/(?P<pk>[0-9]+)/(?P<hash>[a-zA-Z0-9]+)$', views.UserDevice.as_view()),
    ### CONTENT
    # ex: /api/content/user/3
    url(r'^content/user/(?P<pk>[0-9]+)$', views.ContentByUser.as_view()),
    # ex: /api/content/pages/1
    url(r'^content/pages/(?P<pk>[0-9]+)$', views.ContentPages.as_view()),
    # ex: /api/content/play/1/1/1
    url(r'^content/play/(?P<pk>[0-9]+)/(?P<ct>[0-9]+)/(?P<pg>[0-9]+)$', views.PlayContent.as_view()),
    # # ex: /api/content/name/1
    # url(r'^content/name/(?P<pk>[0-9]+)$', views.ContentNames.as_view()),
    # # ex: /api/content/filepath/1
    # url(r'^content/filepath/(?P<pk>[0-9]+)$', views.ContentFilePath.as_view()),


    # url(r'^device/gcm/?$', GCMDeviceViewSet.as_view({'post': 'create'}), name='create_gcm_device'),
    # url(r'^attribute/$', views.AttributeList.as_view()),
    # url(r'^attribute/(?P<pk>[0-9]+)/$', views.AttributeDetails.as_view()),
    # url(r'^attribute/profile/$', views.AttributePost.as_view()),
    # url(r'^attribute/profile/(?P<pk>[0-9]+)/$', views.AttributeByProfile.as_view()),
    # url(r'^profile/$', views.ProfileList.as_view()),
    # url(r'^profile/(?P<pk>[0-9]+)$', views.ProfileDetails.as_view()),
    # url(r'^profile/user/$', views.ProfilePost.as_view()),
    # url(r'^profile/user/(?P<pk>[0-9]+)$', views.UserProfileList.as_view()),
    # url(r'^profile/relation/$', views.MakeRelation.as_view()),
    # url(r'^profile/relation/(?P<pk>[0-9]+)/$', views.Relations.as_view()),
    # url(r'^profile/relation/user/(?P<pk>[0-9]+)/$', views.RelationsByUser.as_view()),
    # url(r'^user/$', views.UserList.as_view()),
    # url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetails.as_view()),
    # url(r'^user/profile/(?P<pk>[0-9]+)/$', views.UserByProfile.as_view()),

    # url(r'^choices/attributes/$', views.ProfilePossibleAttributes.as_view()),
    # url(r'^choices/colors/$', views.ColorsAttributes.as_view()),

]


