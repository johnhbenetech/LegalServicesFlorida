from django.conf.urls import include, url
from .views import ProviderUpdateFormView, ProviderUpdateResultView #, UpdatesStatus
from .tables import UpdatesTable
from . import views

urlpatterns = [
    url(r'^update/$', ProviderUpdateFormView.as_view(success_url='/provider/update/result'), name='update'),
    url(r'^update/result/$', ProviderUpdateResultView.as_view(), name='result'),
#    url(r'^myupdates/$', UpdatesStatus.as_view(), name='myupdates'),
    url(r'^myupdates/$', views.myupdates, name='myupdates'),
]