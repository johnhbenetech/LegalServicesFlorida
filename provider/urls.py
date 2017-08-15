from django.conf.urls import include, url
from .views import ProviderUpdateFormView, ProviderUpdateResultView, ProviderNoProvidersResultView
from .tables import UpdatesTable
from . import views
from django_filters.views import FilterView
from .filters import ProviderFilter

urlpatterns = [
    url(r'^update/$', ProviderUpdateFormView.as_view(success_url='/provider/update/result'), name='update'),
    url(r'^update/result/$', ProviderUpdateResultView.as_view(), name='result'),
    url(r'^update/noproviders/$', ProviderNoProvidersResultView.as_view(), name='no_providers'),
    url(r'^myupdates/$', views.myupdates, name='myupdates'),
    url(r'^search/$', FilterView.as_view(filterset_class=ProviderFilter, template_name='search/provider_list.html'), name='search'),

]