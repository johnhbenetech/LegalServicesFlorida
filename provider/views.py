from django.views import generic
from .models import Provider, ProviderUpdate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django_tables2 import MultiTableMixin, RequestConfig, SingleTableView
from .tables import UpdatesTable
from django.contrib.auth.views import login as contrib_login3


def login(request):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
    return contrib_login(request)
        
class ProviderUpdateFormView(LoginRequiredMixin, generic.CreateView):
    model = ProviderUpdate

    fields = ['provider', 'name', 'phone', 'address', 'description', 'price', ]

    def get_form(self, form_class=None): 
        form = super(generic.CreateView, self).get_form(form_class)
        form.fields['provider'].queryset = Provider.objects.filter(owner = self.request.user)

        provider_id = self.request.GET.get('provider_id', False)

        if provider_id:
            provider = Provider.objects.get(pk=provider_id)
            form.fields['provider'].initial = provider.id
            form.fields['name'].initial = provider.name
            form.fields['phone'].initial = provider.phone
            form.fields['address'].initial = provider.address
            form.fields['description'].initial = provider.description
            form.fields['price'].initial = provider.price

        return form

    def get(self, request):
        result = super(generic.CreateView, self).get(request)

        providers = Provider.objects.filter(owner = self.request.user)
        provider_id = request.GET.get('provider_id', False)

        if providers.count() == 1 and not provider_id:
            provider = providers[0]
            return HttpResponseRedirect('%s?provider_id=%s' % (reverse('provider:update'), provider.id))

        return result

    
#class UpdatesStatus(LoginRequiredMixin, SingleTableView):
#    model = ProviderUpdate
#    template_name = 'myupdates.html'
#    table_class = UpdatesTable

def myupdates(request):
    table = UpdatesTable(ProviderUpdate.objects.filter(provider_id__owner = request.user))
    RequestConfig(request).configure(table)
    return render(request, 'myupdates.html', {'table': table})


class ProviderUpdateResultView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'provider/providerupdate_form_result.html'
    
    

