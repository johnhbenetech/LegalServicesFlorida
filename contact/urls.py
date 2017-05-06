from django.conf.urls import include, url
from .views import ContactUpdateFormView, ContactUpdateResultView

urlpatterns = [
    url(r'^update/$', ContactUpdateFormView.as_view(success_url='/contact/update/result'), name='update'),
    url(r'^update/result/$', ContactUpdateResultView.as_view(), name='result'),
]