from django.conf.urls import include, url
from .views import HomepageView

urlpatterns = [
    url(r'^$', HomepageView.as_view(), name='homepage'),
]