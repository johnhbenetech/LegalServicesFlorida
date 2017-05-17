from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from .views import HomepageView

urlpatterns = [
    url(r'^$', auth_views.LoginView.as_view(redirect_authenticated_user=True),name='login'),
]