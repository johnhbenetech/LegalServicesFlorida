from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django_tables2 import RequestConfig

from .filters import ProviderFilter
from .forms import ProviderUpdateForm, BaseLocationUpdateFormset, PhysicalAddressUpdateFormset
from .models import Provider, ProviderUpdate, LocationUpdate, ContactUpdate
from .tables import UpdatesTable
from functools import partial, wraps


def login(request):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
    return contrib_login(request)


class ProviderUpdateFormView(LoginRequiredMixin, generic.CreateView):
    model = ProviderUpdate
    form_class = ProviderUpdateForm

    def get_location_update_formset(self, extra):
        return inlineformset_factory(ProviderUpdate, LocationUpdate, extra=extra,
                              can_delete=0, can_order=0,
                              formset=BaseLocationUpdateFormset,
                              fields=('location', 'name', 'alternate_name', 'description',
                                      'transportation', 'latitude', 'longtitude',),
                              widgets={'location': forms.HiddenInput()})

    def get_contact_update_formset(self, extra):
        return inlineformset_factory(LocationUpdate, ContactUpdate, extra=extra,
                                                     can_delete=False, can_order=False,
                                                     fields=('contact', 'name', 'title', 'department', 'email',),
                                                     widgets={'contact': forms.HiddenInput()})

    def populate_initial_phone_update(self, contact_form, contact):
        phones = contact.phones.all()
        contact_form.phone_update.extra = phones.count()

        for phone_idx, phone in enumerate(phones):
            contact_form.phone_update.forms[phone_idx]['number'].initial = phone.number
            contact_form.phone_update.forms[phone_idx]['extension'].initial = phone.extension
            contact_form.phone_update.forms[phone_idx]['type'].initial = phone.type
            contact_form.phone_update.forms[phone_idx]['department'].initial = phone.department
            contact_form.phone_update.forms[phone_idx]['languages'].initial = phone.languages.all()
            contact_form.phone_update.forms[phone_idx]['description'].initial = phone.description
            contact_form.phone_update.forms[phone_idx]['phone'].initial = phone

    def get(self, request, *args, **kwargs):
        """
        Redirect to single provider
        """
        providers = Provider.objects.filter(owner=self.request.user)
        provider_id = request.GET.get('provider_id', False)

        provider = None

        if providers.count() == 1 and not provider_id:
            provider = providers[0]
            return HttpResponseRedirect('%s?provider_id=%s' % (reverse('provider:update'), provider.id))

        provider_id = self.request.GET.get('provider_id', False)

        if provider_id:
            provider = Provider.objects.get(pk=provider_id)
        else:
            return HttpResponseRedirect(reverse('provider:no_providers'))
        """
        Attach formsets with children
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        extra_location_updates = provider.locations.count()
        LocationUpdateFormset = self.get_location_update_formset(extra_location_updates)

        location_update_form_initial = []
        for location in provider.locations.all():
            location_initial = {
                'location': location.id,
                'name': location.name,
                'alternate_name': location.alternate_name,
                'description': location.description,
                'transportation': location.transportation,
                'latitude': location.latitude,
                'longtitude': location.longtitude,
            }
            location_update_form_initial.append(location_initial)

        location_update_form = LocationUpdateFormset(initial=location_update_form_initial)

        for location_idx, location in enumerate(provider.locations.all()):
            contacts = location.contacts.all()
            physical_addresses = [location.physical_address]

            location_update_form[location_idx].contact_update.extra = contacts.count()
            location_update_form[location_idx].physical_address_update.extra = 1

            for contact_idx,contact in enumerate(contacts):
                location_update_form[location_idx].contact_update.forms[contact_idx]['name'].initial = contact.name
                location_update_form[location_idx].contact_update.forms[contact_idx]['title'].initial = contact.title
                location_update_form[location_idx].contact_update.forms[contact_idx]['department'].initial = contact.department
                location_update_form[location_idx].contact_update.forms[contact_idx]['email'].initial = contact.email
                location_update_form[location_idx].contact_update.forms[contact_idx]['contact'].initial = contact
                self.populate_initial_phone_update(location_update_form[location_idx].contact_update.forms[contact_idx], contact)

            for physical_address_idx,physical_address in enumerate(physical_addresses):
                location_update_form[location_idx].physical_address_update.forms[physical_address_idx]['attention'].initial = physical_address.attention
                location_update_form[location_idx].physical_address_update.forms[physical_address_idx]['address_1'].initial = physical_address.address_1
                location_update_form[location_idx].physical_address_update.forms[physical_address_idx]['address_2'].initial = physical_address.address_2
                location_update_form[location_idx].physical_address_update.forms[physical_address_idx]['address_3'].initial = physical_address.address_3
                location_update_form[location_idx].physical_address_update.forms[physical_address_idx]['address_4'].initial = physical_address.address_4
                location_update_form[location_idx].physical_address_update.forms[physical_address_idx]['city'].initial = physical_address.city
                location_update_form[location_idx].physical_address_update.forms[physical_address_idx]['region'].initial = physical_address.region
                location_update_form[location_idx].physical_address_update.forms[physical_address_idx]['state_province'].initial = physical_address.state_province
                location_update_form[location_idx].physical_address_update.forms[physical_address_idx]['postal_code'].initial = physical_address.postal_code
                location_update_form[location_idx].physical_address_update.forms[physical_address_idx]['physical_address'].initial = physical_address


        return self.render_to_response(
            self.get_context_data(form=form, location_update_form=location_update_form)
        )

    def post(self, request, *args, **kwargs):

        provider_id = self.request.GET.get('provider_id', False)

        if provider_id:
            provider = Provider.objects.get(pk=provider_id)

        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        extra_location_updates = provider.locations.count()
        LocationUpdateFormset = self.get_location_update_formset(0)

        location_update_form = LocationUpdateFormset(self.request.POST)


        for location_idx, location in enumerate(provider.locations.all()):
            contacts = location.contacts.all()

            location_update_form[location_idx].contact_update.extra = contacts.count()
            #location_update_form[location_idx].physical_address_update.extra = 1

        if (form.is_valid() and location_update_form.is_valid()):
            return self.form_valid(form, location_update_form)
        else:
            return self.form_invalid(form, location_update_form)

    def form_valid(self, form, location_update_form):
        self.object = form.save()
        self.object.is_emailed = False
        self.object.save()
        location_update_form.instance = self.object
        location_update_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, location_update_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  location_update_form=location_update_form))

    def get_form(self, form_class=None):
        form = super(generic.CreateView, self).get_form(form_class)

        form.fields['provider'].queryset = Provider.objects.filter(owner=self.request.user)

        provider_id = self.request.GET.get('provider_id', False)

        if provider_id:
            provider = Provider.objects.get(pk=provider_id)
            form.fields['provider'].initial = provider.id
            form.fields['organization_name'].initial = provider.organization_name
            form.fields['phone'].initial = provider.phone
            form.fields['website_url'].initial = provider.website_url
            form.fields['primary_address'].initial = provider.primary_address
            form.fields['description'].initial = provider.description
            form.fields['price'].initial = provider.price
            form.fields['counties'].initial = provider.counties.all()

        return form


# class UpdatesStatus(LoginRequiredMixin, SingleTableView):
#    model = ProviderUpdate
#    template_name = 'myupdates.html'
#    table_class = UpdatesTable

def myupdates(request):
    table = UpdatesTable(ProviderUpdate.objects.filter(provider_id__owner=request.user))
    RequestConfig(request).configure(table)
    return render(request, 'myupdates.html', {'table': table})


class ProviderUpdateResultView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'provider/providerupdate_form_result.html'

class ProviderNoProvidersResultView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'provider/providerupdate_no_providers.html'

def search(request):
    provider_list = Provider.objects.all()
    provider_filter = ProviderFilter(request.GET, queryset=provider_list)
    return render(request, 'search/provider_list.html', {'filter': provider_filter})
