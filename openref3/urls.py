from django.contrib import admin
from . import views

from django.conf.urls import url, include
from rest_framework import routers
from django.contrib.auth import views as auth_views
from service.rest_api import ServiceList, ServiceUpdateViewSet, OrganizationList
from rest_framework_swagger.views import get_swagger_view


router = routers.DefaultRouter()
router.register(r'services', ServiceList, 'services')
router.register(r'service_updates', ServiceUpdateViewSet, 'service-updates')
router.register(r'organizations', OrganizationList, 'organizations')



urlpatterns = [
    url(r'^', include('homepage.urls')),
    url(r'^service/', include('service.urls', namespace='service')),
    url(r'^token/', include('apitoken.urls', namespace='token')),
    url(r'^login/',auth_views.LoginView.as_view(redirect_authenticated_user=True),name='login'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^email/$', views.email, name='email'),
    url(r'^docs/',  get_swagger_view()),
    url(r'^api/v1/', include(router.urls, namespace='api')),
    url(r'^select2/', include('select2.urls')),
    url(r'^nested_admin/', include('nested_admin.urls')),
]
