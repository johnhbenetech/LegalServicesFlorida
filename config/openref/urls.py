from django.conf.urls import url
from . import views
from django_filters.views import FilterView
from .filters import ProviderFilter
 
urlpatterns = [
    url(r'^providers/$', views.ProviderList.as_view()),
    url(r'^providers/(?P<provider_id>[0-9]+)/$', views.ProviderDetail.as_view()),
    url(
        r'^providers/(?P<provider_id>[0-9]+)/updates/$',
        views.ProviderUpdateList.as_view()
    ),
    url(
        r'^providers/(?P<provider_id>[0-9]+)/updates/(?P<providerupdate_id>[0-9]+)/$',
        views.ProviderUpdateDetail.as_view()
    ),
	url(r'^search/$', FilterView.as_view(filterset_class=ProviderFilter,
        template_name='search/provider_list.html'), name='search'),
]