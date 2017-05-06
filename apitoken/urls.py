from django.conf.urls import include, url
from rest_framework.authtoken.views import obtain_auth_token
from .views import TokenGetView


urlpatterns = [
    url(r'^get/$', TokenGetView.as_view(), name='get'),
    url(r'^auth/', obtain_auth_token),
]