"""URL configuration for the CusDeb API Users application. """

from django.conf.urls import url

from . import views


app_name = 'social'

urlpatterns = [
    # authentication / association
    url(r'^login/(?P<backend>[^/]+)/?$', views.auth, name='begin'),
    url(r'^complete/(?P<backend>[^/]+)/?$', views.complete, name='complete'),
    # disconnection
    url(r'^disconnect/(?P<backend>[^/]+)/?$', views.disconnect, name='disconnect'),
    url(r'^disconnect/(?P<backend>[^/]+)/(?P<association_id>\d+)/?$', views.disconnect,
        name='disconnect_individual'),

    url('token/?$', views.GetTokenForSocial.as_view(), name='token-obtain-pair-social'),
]
