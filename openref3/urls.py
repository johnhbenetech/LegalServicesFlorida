from django.contrib import admin

from django.conf.urls import url, include
from rest_framework import routers
from django.contrib.auth import views as auth_views
from contact.rest_api import ContactList, ContactUpdateViewSet

router = routers.DefaultRouter()
router.register(r'contacts', ContactList, 'contacts')
router.register(r'contact_updates', ContactUpdateViewSet, 'contact-updates')

urlpatterns = [
    url(r'^', include('homepage.urls')),
    url(r'^contact/', include('contact.urls', namespace='contact')),
    url(r'^token/', include('apitoken.urls', namespace='token')),
    url(r'^login/',auth_views.LoginView.as_view(redirect_authenticated_user=True),name='login'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(router.urls, namespace='api')),
]
