from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django_tables2 import RequestConfig

from .filters import ServiceFilter
from .forms import ServiceUpdateForm, BaseEligibilityUpdateFormset, BasePaymentAcceptedUpdateFormset, BaseRequiredDocumentUpdateFormset, BaseServiceAreaUpdateFormset, BaseLocationUpdateFormset, BaseRegularScheduleUpdateFormset, BaseHolidayScheduleUpdateFormset
from .models import Service, ServiceUpdate, PaymentAcceptedUpdate, RequiredDocumentUpdate, ServiceAreaUpdate, EligibilityUpdate, LocationUpdate,  ContactUpdate, PhysicalAddressUpdate, RegularScheduleUpdate, HolidayScheduleUpdate
from .tables import UpdatesTable
from functools import partial, wraps


def login(request):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
    return contrib_login(request)

class DateInput(forms.DateInput):
    input_type = 'date'
    
class TimeInput(forms.TimeInput):
    input_type = 'time'    
    
    
class ServiceUpdateFormView(LoginRequiredMixin, generic.CreateView):
    model = ServiceUpdate
    form_class = ServiceUpdateForm
    
    
    def get_eligibility_update_formset(self, extra):
        return inlineformset_factory(ServiceUpdate, EligibilityUpdate, extra=extra,
                              can_delete=0, can_order=0,
                              formset=BaseEligibilityUpdateFormset,
                              fields=('eligibility_record','eligibility_details',),
                              widgets={'eligibility_record': forms.HiddenInput()})
                              
                              
    def get_paymentaccepted_update_formset(self, extra):
        return inlineformset_factory(ServiceUpdate, PaymentAcceptedUpdate, extra=extra,
                              can_delete=0, can_order=0,
                              formset=BasePaymentAcceptedUpdateFormset,
                              fields=('payment_record','payment',),
                              widgets={'payment_record': forms.HiddenInput()})
                              
    def get_requireddocument_update_formset(self, extra):
        return inlineformset_factory(ServiceUpdate, RequiredDocumentUpdate, extra=extra,
                              can_delete=0, can_order=0,
                              formset=BaseRequiredDocumentUpdateFormset,
                              fields=('required_document_record','document',),
                              widgets={'required_document_record': forms.HiddenInput()})
                              
    def get_servicearea_update_formset(self, extra):
        return inlineformset_factory(ServiceUpdate, ServiceAreaUpdate, extra=extra,
                              can_delete=0, can_order=0,
                              formset=BaseServiceAreaUpdateFormset,
                              fields=('area_record','area', 'description',),
                              widgets={'area_record': forms.HiddenInput()})

    def get_regularschedule_update_formset(self, extra):
        return inlineformset_factory(ServiceUpdate, RegularScheduleUpdate, extra=extra,
                              can_delete=0, can_order=0,
                              formset=BaseRegularScheduleUpdateFormset,
                              fields=('regular_schedule_record','weekday', 'from_hour', 'to_hour', 'closed'),
                              widgets={'regular_schedule_record': forms.HiddenInput(),'from_hour': TimeInput(),'to_hour': TimeInput()})   
                              
    def get_holidayschedule_update_formset(self, extra):
        return inlineformset_factory(ServiceUpdate, HolidayScheduleUpdate, extra=extra,
                              can_delete=0, can_order=0,
                              formset=BaseHolidayScheduleUpdateFormset,
                              fields=('holiday_schedule_record','day', 'from_hour', 'to_hour', 'closed'),
                              widgets={'holiday_schedule_record': forms.HiddenInput(),'day': DateInput(),'from_hour': TimeInput(),'to_hour': TimeInput()})                                


                              
    def get_location_update_formset(self, extra):
        return inlineformset_factory(ServiceUpdate, LocationUpdate, extra=extra,
                              can_delete=0, can_order=0,
                              formset=BaseLocationUpdateFormset,
                              fields=('location_record', 'name', 'alternate_name', 'description',
                                      'transportation', 'latitude', 'longitude',),
                              widgets={'location_record': forms.HiddenInput()})

    def get_contact_update_formset(self, extra):
        return inlineformset_factory(LocationUpdate, ContactUpdate, extra=extra,
                                                     can_delete=False, can_order=False,
                                                     fields=('contact_record', 'name', 'title', 'department', 'email',),
                                                     widgets={'contact_record': forms.HiddenInput()})

    def get_physical_address_update_formset(self, extra):
        return inlineformset_factory(LocationUpdate, PhysicalAddressUpdate, extra=extra,
                                                     can_delete=False, can_order=False,
                                                     fields=('physical_address_record', 'attention', 'address_1', 'address_2', 'address_3', 'address_4', 'city', 'region', 'state_province', 'postal_code',),
                                                     widgets={'physical_address_record': forms.HiddenInput()})

                                                                                                          
    def populate_initial_phone_update(self, contact_form, contact_record):
        phones = contact_record.phones.all()
        contact_form.phone_update.extra = phones.count()

        for phone_idx, phone_record in enumerate(phones):
            contact_form.phone_update.forms[phone_idx]['number'].initial = phone_record.number
            contact_form.phone_update.forms[phone_idx]['extension'].initial = phone_record.extension
            contact_form.phone_update.forms[phone_idx]['type'].initial = phone_record.type
            contact_form.phone_update.forms[phone_idx]['department'].initial = phone_record.department
            contact_form.phone_update.forms[phone_idx]['languages'].initial = phone_record.languages.all()
            contact_form.phone_update.forms[phone_idx]['description'].initial = phone_record.description
            contact_form.phone_update.forms[phone_idx]['phone_record'].initial = phone_record                              

    def get(self, request, *args, **kwargs):
        """
        Redirect to single provider
        """
        services = Service.objects.filter(owner=self.request.user)
        service_id = request.GET.get('service_id', False)

        service = None
        
        if services.count() >= 1 and not service_id:
            service = services[0]
            return HttpResponseRedirect('%s?service_id=%s' % (reverse('service:update'), service.id))

        service_id = self.request.GET.get('service_id', False)


        if service_id:
            if services.filter(id=service_id).exists():
                service = Service.objects.get(pk=service_id)
            else:
                return HttpResponseRedirect(reverse('service:not_found'))    
        else:
            return HttpResponseRedirect(reverse('service:no_services'))
        """
        Attach formsets with children
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        
        
        
        extra_eligibility_updates = service.eligibilities.count()
        EligibilityUpdateFormset = self.get_eligibility_update_formset(extra_eligibility_updates)

        eligibility_update_form_initial = []
        for eligibility in service.eligibilities.all():
            eligibility_initial = {
                'eligibility_record': eligibility.id,
                'eligibility_details': eligibility.eligibility_details,
            }
            eligibility_update_form_initial.append(eligibility_initial)

        eligibility_update_form = EligibilityUpdateFormset(initial=eligibility_update_form_initial)
        
        
        extra_paymentaccepted_updates = service.payments.count()
        PaymentAcceptedUpdateFormset = self.get_paymentaccepted_update_formset(extra_paymentaccepted_updates)

        paymentaccepted_update_form_initial = []
        for paymentaccepted in service.payments.all():
            paymentaccepted_initial = {
                'payment_record': paymentaccepted.id,
                'payment': paymentaccepted.payment,
            }
            paymentaccepted_update_form_initial.append(paymentaccepted_initial)

        paymentaccepted_update_form = PaymentAcceptedUpdateFormset(initial=paymentaccepted_update_form_initial)

        
        
        extra_requireddocument_updates = service.documents.count()
        RequiredDocumentUpdateFormset = self.get_requireddocument_update_formset(extra_requireddocument_updates)        
        
        requireddocument_update_form_initial = []
        for requireddocument in service.documents.all():
            requireddocument_initial = {
                'required_document_record': requireddocument.id,
                'document': requireddocument.document,
            }
            requireddocument_update_form_initial.append(requireddocument_initial)

        requireddocument_update_form = RequiredDocumentUpdateFormset(initial=requireddocument_update_form_initial)
        
        
        

        extra_servicearea_updates = service.areas.count()
        ServiceAreaUpdateFormset = self.get_servicearea_update_formset(extra_servicearea_updates)        
        
        servicearea_update_form_initial = []
        for servicearea in service.areas.all():
            servicearea_initial = {
                'area_record': servicearea.id,
                'area': servicearea.area.all(),
                'description': servicearea.description, 
            }
            servicearea_update_form_initial.append(servicearea_initial)

        servicearea_update_form = ServiceAreaUpdateFormset(initial=servicearea_update_form_initial)
        
        
        extra_regularschedule_updates = service.regular_schedule.count()
        RegularScheduleUpdateFormset = self.get_regularschedule_update_formset(extra_regularschedule_updates)        
        
        regularschedule_update_form_initial = []
        for regularschedule in service.regular_schedule.all():
            regularschedule_initial = {
                'regular_schedule_record': regularschedule.id,
                'weekday': regularschedule.weekday,
                'from_hour': regularschedule.from_hour, 
                'to_hour': regularschedule.to_hour,
                'closed': regularschedule.closed,
            }
            regularschedule_update_form_initial.append(regularschedule_initial)

        regularschedule_update_form = RegularScheduleUpdateFormset(initial=regularschedule_update_form_initial)
        
        
        extra_holidayschedule_updates = service.holiday_schedule.count()
        HolidayScheduleUpdateFormset = self.get_holidayschedule_update_formset(extra_holidayschedule_updates)        
        
        holidayschedule_update_form_initial = []
        for holidayschedule in service.holiday_schedule.all():
            holidayschedule_initial = {
                'holiday_schedule_record': holidayschedule.id,
                'day': holidayschedule.day,
                'from_hour': holidayschedule.from_hour, 
                'to_hour': holidayschedule.to_hour,
                'closed': holidayschedule.closed,
            }
            holidayschedule_update_form_initial.append(holidayschedule_initial)

        holidayschedule_update_form = HolidayScheduleUpdateFormset(initial=holidayschedule_update_form_initial)        
        
        extra_location_updates = service.locations.count()
        LocationUpdateFormset = self.get_location_update_formset(extra_location_updates)
        location_update_form_initial = []
        
        for location in service.locations.all():
            location_initial = {
                'location_record': location.id,
                'name': location.name,
                'alternate_name': location.alternate_name,
                'description': location.description,
                'transportation': location.transportation,
                'latitude': location.latitude,
                'longitude': location.longitude,
            }
            location_update_form_initial.append(location_initial)

        location_update_form = LocationUpdateFormset(initial=location_update_form_initial)

        for location_idx, location_record in enumerate(service.locations.all()):
            contacts = location_record.contacts.all()
            physical_addresses = location_record.physical_addresses.all()

            location_update_form[location_idx].contact_update.extra = contacts.count()
            location_update_form[location_idx].physical_address_update.extra = physical_addresses.count()

            for contact_idx,contact_record in enumerate(contacts):
                location_update_form[location_idx].contact_update.forms[contact_idx]['name'].initial = contact_record.name
                location_update_form[location_idx].contact_update.forms[contact_idx]['title'].initial = contact_record.title
                location_update_form[location_idx].contact_update.forms[contact_idx]['department'].initial = contact_record.department
                location_update_form[location_idx].contact_update.forms[contact_idx]['email'].initial = contact_record.email
                location_update_form[location_idx].contact_update.forms[contact_idx]['contact_record'].initial = contact_record
                self.populate_initial_phone_update(location_update_form[location_idx].contact_update.forms[contact_idx], contact_record)

            for physical_address_idx,physical_address_record in enumerate(physical_addresses):
                location_update_form[location_idx].physical_address_update.forms[physical_address_idx]['attention'].initial = physical_address_record.attention
                location_update_form[location_idx].physical_address_update.forms[physical_address_idx]['address_1'].initial = physical_address_record.address_1
                location_update_form[location_idx].physical_address_update.forms[physical_address_idx]['address_2'].initial = physical_address_record.address_2
                location_update_form[location_idx].physical_address_update.forms[physical_address_idx]['address_3'].initial = physical_address_record.address_3
                location_update_form[location_idx].physical_address_update.forms[physical_address_idx]['address_4'].initial = physical_address_record.address_4
                location_update_form[location_idx].physical_address_update.forms[physical_address_idx]['city'].initial = physical_address_record.city
                location_update_form[location_idx].physical_address_update.forms[physical_address_idx]['region'].initial = physical_address_record.region
                location_update_form[location_idx].physical_address_update.forms[physical_address_idx]['state_province'].initial = physical_address_record.state_province
                location_update_form[location_idx].physical_address_update.forms[physical_address_idx]['postal_code'].initial = physical_address_record.postal_code
                location_update_form[location_idx].physical_address_update.forms[physical_address_idx]['physical_address_record'].initial = physical_address_record



        return self.render_to_response(
            self.get_context_data(form=form, eligibility_update_form=eligibility_update_form, paymentaccepted_update_form=paymentaccepted_update_form, requireddocument_update_form=requireddocument_update_form, servicearea_update_form=servicearea_update_form, location_update_form=location_update_form, regularschedule_update_form=regularschedule_update_form,  holidayschedule_update_form=holidayschedule_update_form)
        )

    def post(self, request, *args, **kwargs):

        service_id = self.request.GET.get('service_id', False)

        if service_id:
            service = Service.objects.get(pk=service_id)

        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        extra_eligibility_updates = service.eligibilities.count()
        EligibilityUpdateFormset = self.get_eligibility_update_formset(0)
        eligibility_update_form = EligibilityUpdateFormset(self.request.POST)
        
        extra_paymentaccepted_updates = service.payments.count()
        PaymentAcceptedUpdateFormset = self.get_paymentaccepted_update_formset(0)
        paymentaccepted_update_form = PaymentAcceptedUpdateFormset(self.request.POST)

        extra_requireddocument_updates = service.documents.count()
        RequiredDocumentUpdateFormset = self.get_requireddocument_update_formset(0)
        requireddocument_update_form = RequiredDocumentUpdateFormset(self.request.POST)
        
        extra_servicearea_updates = service.areas.count()
        ServiceAreaUpdateFormset = self.get_servicearea_update_formset(0)
        servicearea_update_form = ServiceAreaUpdateFormset(self.request.POST)  
        
        extra_regularschedule_updates = service.regular_schedule.count()
        RegularScheduleUpdateFormset = self.get_regularschedule_update_formset(0)
        regularschedule_update_form = RegularScheduleUpdateFormset(self.request.POST)


        extra_holidayschedule_updates = service.holiday_schedule.count()
        HolidayScheduleUpdateFormset = self.get_holidayschedule_update_formset(0)
        holidayschedule_update_form = HolidayScheduleUpdateFormset(self.request.POST)         

        
        extra_location_updates = service.locations.count()
        LocationUpdateFormset = self.get_location_update_formset(0)

        location_update_form = LocationUpdateFormset(self.request.POST)


        for location_idx, location in enumerate(service.locations.all()):
            contacts = location.contacts.all()
            physical_addresses = location.physical_addresses.all()
            location_update_form[location_idx].contact_update.extra = contacts.count()
            location_update_form[location_idx].physical_address_update.extra = physical_addresses.count()

        if (form.is_valid() and eligibility_update_form.is_valid() and paymentaccepted_update_form.is_valid() and requireddocument_update_form.is_valid() and servicearea_update_form.is_valid() and location_update_form.is_valid() and regularschedule_update_form.is_valid() and holidayschedule_update_form.is_valid()):
            return self.form_valid(form, eligibility_update_form, paymentaccepted_update_form, requireddocument_update_form, servicearea_update_form, location_update_form, regularschedule_update_form, holidayschedule_update_form)
        else:
            return self.form_invalid(form, eligibility_update_form, paymentaccepted_update_form, requireddocument_update_form, servicearea_update_form, location_update_form, regularschedule_update_form, holidayschedule_update_form)

    def form_valid(self, form, eligibility_update_form, paymentaccepted_update_form, requireddocument_update_form, servicearea_update_form, location_update_form, regularschedule_update_form, holidayschedule_update_form):
        self.object = form.save()
        self.object.is_emailed = False
        self.object.save()
        
        eligibility_update_form.instance = self.object
        eligibility_update_form.save()
        
        paymentaccepted_update_form.instance = self.object
        paymentaccepted_update_form.save()
        
        requireddocument_update_form.instance = self.object
        requireddocument_update_form.save()
        
        servicearea_update_form.instance = self.object
        servicearea_update_form.save()
        
        regularschedule_update_form.instance = self.object
        regularschedule_update_form.save()
        
        holidayschedule_update_form.instance = self.object
        holidayschedule_update_form.save()        
        
        location_update_form.instance = self.object
        location_update_form.save()        
        
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, eligibility_update_form, paymentaccepted_update_form,requireddocument_update_form,servicearea_update_form, location_update_form, regularschedule_update_form, holidayschedule_update_form ):
        return self.render_to_response(
            self.get_context_data(form=form,eligibility_update_form=eligibility_update_form,paymentaccepted_update_form=paymentaccepted_update_form,requireddocument_update_form=requireddocument_update_form, servicearea_update_form=servicearea_update_form, location_update_form=location_update_form,regularschedule_update_form=regularschedule_update_form, holidayschedule_update_form=holidayschedule_update_form))

    def get_form(self, form_class=None):
        form = super(generic.CreateView, self).get_form(form_class)

        form.fields['service'].queryset = Service.objects.filter(owner=self.request.user)

        service_id = self.request.GET.get('service_id', False)

        if service_id:
            service = Service.objects.get(pk=service_id)
            form.fields['service'].initial = service.id
            form.fields['name'].initial = service.name
            form.fields['alternate_name'].initial = service.alternate_name
            form.fields['description'].initial = service.description
            form.fields['url'].initial = service.url
            form.fields['email'].initial = service.email
            form.fields['status'].initial = service.status
            form.fields['interpretation_services'].initial = service.interpretation_services.all()
            form.fields['application_process'].initial = service.application_process
            form.fields['wait_time'].initial = service.wait_time
            form.fields['fees'].initial = service.fees
            form.fields['accredidations'].initial = service.accredidations
            form.fields['licenses'].initial = service.licenses
            form.fields['taxonomy_ids'].initial = service.taxonomy_ids.all()
            

        return form


# class UpdatesStatus(LoginRequiredMixin, SingleTableView):
#    model = ProviderUpdate
#    template_name = 'myupdates.html'
#    table_class = UpdatesTable

def myupdates(request):
    table = UpdatesTable(ServiceUpdate.objects.filter(service_id__owner=request.user))
    RequestConfig(request).configure(table)
    return render(request, 'myupdates.html', {'table': table})   
    

class ServiceUpdateResultView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'service/serviceupdate_form_result.html'

class ServiceNoServicesResultView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'service/serviceupdate_no_services.html'
    
class ServiceNotFoundResultView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'service/serviceupdate_not_found.html'

def search(request):
    service_list = Service.objects.all()
    service_filter = ServiceFilter(request.GET, queryset=service_list)
    return render(request, 'search/service_list.html', {'filter': service_filter})
