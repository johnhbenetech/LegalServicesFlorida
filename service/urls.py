from django.conf.urls import include, url
from .views import ServiceUpdateFormView, ServiceUpdateResultView, ServiceNoServicesResultView, ServiceNotFoundResultView
from .tables import UpdatesTable
from . import views
from django_filters.views import FilterView
from .filters import ServiceFilter

urlpatterns = [
    url(r'^update/$', ServiceUpdateFormView.as_view(success_url='/service/update/result'), name='update'),
    url(r'^update/result/$', ServiceUpdateResultView.as_view(), name='result'),
    url(r'^update/noservices/$', ServiceNoServicesResultView.as_view(), name='no_services'),
    url(r'^update/notfound/$', ServiceNotFoundResultView.as_view(), name='not_found'),    
    url(r'^myupdates/$', views.myupdates, name='myupdates'),
    url(r'^search/$', FilterView.as_view(filterset_class=ServiceFilter, template_name='search/service_list.html'), name='search'),

]