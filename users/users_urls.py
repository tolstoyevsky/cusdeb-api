from django.urls import re_path

from .views import WhoAmIView


urlpatterns = [  # pylint: disable=invalid-name
    re_path('whoami/?$', WhoAmIView.as_view(), name='who-am-i'),
]
