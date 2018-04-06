from django.conf.urls import url
from . import views
from django.contrib.auth.views import login

urlpatterns = [

    url(r'^login/$', login, {'template_name' : 'testapp/index.html'}),
    url(r'^login/check/$', views.backend.__init__),
    url(r'^login/get/$', views.backend.getcont),
    url(r'^login/getback/$', views.backend.getback),
    url(r'^login/getcontag/$', views.backend.getcontag),
    url(r'^login/createbuck/$', views.backend.createbucket),
    url(r'^login/createbsite/$', views.backend.createbsite),
    url(r'^login/deletebucket/$', views.backend.deletebucket),
    url(r'^login/createobject/$', views.backend.createobject),
    url(r'^login/createobjectsite/$', views.backend.createobjectsite),
    url(r'^login/deleteobject/$', views.backend.deleteobject),
    url(r'^login/downloadsite/$', views.backend.downloadsite),
    url(r'^login/download/$', views.backend.download),
    url(r'^login/select/$', views.backend.select),
    url(r'^login/upload/$', views.backend.upload),
    url(r'^login/publish/$', views.backend.publish),
    url(r'^login/errorpublish/$', views.backend.errorpublish),
    url(r'^login/publishsite/$', views.backend.publishsite),
    url(r'^login/profile/$', views.backend.profile),
    url(r'^login/create/$', views.backend.create),

    url(r'^login/chcolorw/$', views.backend.chcolorw),
    url(r'^login/chcolorb/$', views.backend.chcolorb),



]
