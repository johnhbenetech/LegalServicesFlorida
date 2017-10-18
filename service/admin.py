import nested_admin
from django import forms
from django.contrib import admin
from django.core.urlresolvers import reverse
from reversion.admin import VersionAdmin
from .forms import PhoneUpdateForm, PhoneForm
import datetime


from liststyle import ListStyleAdminMixin

from .models import Organization, Service, ServiceUpdate, PaymentAccepted, PaymentAcceptedUpdate, RequiredDocument, RequiredDocumentUpdate, ServiceArea, ServiceAreaUpdate, Eligibility, EligibilityUpdate, Location, PhysicalAddress, Contact, Phone, LocationUpdate, ContactUpdate, PhysicalAddressUpdate, PhoneUpdate, RegularSchedule, RegularScheduleUpdate, HolidaySchedule, HolidayScheduleUpdate

admin.site.site_header = 'My administration'
admin.site.site_title= 'Admin'
admin.site.index_title= 'Admin Actions'



class DefaultFilterMixIn(admin.ModelAdmin):
    def changelist_view(self, request, *args, **kwargs):
        from django.http import HttpResponseRedirect
        if self.default_filters:
            #try:
                test = request.META['HTTP_REFERER'].split(request.META['PATH_INFO'])
                if test and test[-1] and not test[-1].startswith('?'):
                    url = reverse('admin:{}_{}_changelist'.format(self.opts.app_label, self.opts.model_name))
                    filters = []
                    for filter in self.default_filters:
                        key = filter.split('=')[0]
                        if not key in request.GET:
                            filters.append(filter)
                    if filters:                     
                        return HttpResponseRedirect("{}?{}".format(url, "&".join(filters)))
            #except: pass
        return super(DefaultFilterMixIn, self).changelist_view(request, *args, **kwargs) 


"""
Update forms
"""


        
        
class RequiredDocumentUpdateInline(nested_admin.NestedStackedInline):
    model = RequiredDocumentUpdate
    extra = 0
    can_delete = True
    readonly_fields = ('required_document_record','required_document_record_document', )
    fieldsets = (
        (None, {
            'fields': ('required_document_record',),
        }),
        (None, {
            'fields': (
                ('required_document_record_document', 'document',),
            )
        })
    )

    def required_document_record_document(self, obj):
        return obj.required_document_record.document
        
        
class RegularScheduleUpdateInline(nested_admin.NestedStackedInline):
    model = RegularScheduleUpdate
    extra = 0
    can_delete = True
    readonly_fields = ('regular_schedule_record','regular_schedule_record_weekday', 'regular_schedule_record_from_hour', 'regular_schedule_record_to_hour', 'regular_schedule_record_closed', )
    fieldsets = (
        (None, {
            'fields': ('regular_schedule_record',),
        }),
        (None, {
            'fields': (
                ('regular_schedule_record_weekday', 'weekday',),
                ('regular_schedule_record_from_hour', 'from_hour',),
                ('regular_schedule_record_to_hour', 'to_hour',),
                ('regular_schedule_record_closed', 'closed',),
                
            )
        })
    )

    def regular_schedule_record_weekday(self, obj):
        return obj.regular_schedule_record.get_weekday_display() 

    def regular_schedule_record_from_hour(self, obj):
        return str(obj.regular_schedule_record.from_hour.hour) +":"+ str(obj.regular_schedule_record.from_hour.minute)

    def regular_schedule_record_to_hour(self, obj):
        return str(obj.regular_schedule_record.to_hour.hour) +":"+ str(obj.regular_schedule_record.to_hour.minute)

    def regular_schedule_record_closed(self, obj):
        return obj.regular_schedule_record.closed   

class HolidayScheduleUpdateInline(nested_admin.NestedStackedInline):
    model = HolidayScheduleUpdate
    extra = 0
    can_delete = True
    readonly_fields = ('holiday_schedule_record','holiday_schedule_record_day', 'holiday_schedule_record_from_hour', 'holiday_schedule_record_to_hour', 'holiday_schedule_record_closed', )
    fieldsets = (
        (None, {
            'fields': ('holiday_schedule_record',),
        }),
        (None, {
            'fields': (
                ('holiday_schedule_record_day', 'day',),
                ('holiday_schedule_record_from_hour', 'from_hour',),
                ('holiday_schedule_record_to_hour', 'to_hour',),
                ('holiday_schedule_record_closed', 'closed',),
                
            )
        })
    )

    def holiday_schedule_record_day(self, obj):
        return obj.holiday_schedule_record.day 

    def holiday_schedule_record_from_hour(self, obj):
        return str(obj.holiday_schedule_record.from_hour.hour) +":"+ str(obj.holiday_schedule_record.from_hour.minute)

    def holiday_schedule_record_to_hour(self, obj):
        return str(obj.holiday_schedule_record.to_hour.hour) +":"+ str(obj.holiday_schedule_record.to_hour.minute)

    def holiday_schedule_record_closed(self, obj):
        return obj.holiday_schedule_record.closed        

        
class ServiceAreaUpdateInline(nested_admin.NestedStackedInline):
    model = ServiceAreaUpdate
    extra = 0
    can_delete = True
    readonly_fields = ('area_record','area_record_area','area_record_description', )
    fieldsets = (
        (None, {
            'fields': ('area_record',),
        }),
        (None, {
            'fields': (
                ('area_record_area','area',),
                ('area_record_description','description',),
            )
        })
    )

    def area_record_area(self, obj):
        return ", ".join(obj.area_record.area.all().values_list('name', flat=True))

    def area_record_description(self, obj):
        return obj.area_record.description

        
        
class EligibilityUpdateInline(nested_admin.NestedStackedInline):
    model = EligibilityUpdate
    extra = 0
    can_delete = True
    readonly_fields = ('eligibility_record','eligibility_record_eligibility_details', )
    fieldsets = (
        (None, {
            'fields': ('eligibility_record',),
        }),
        (None, {
            'fields': (
                ('eligibility_record_eligibility_details','eligibility_details',),
            )
        })
    )

    def eligibility_record_eligibility_details(self, obj):
        return obj.eligibility_record.eligibility_details
        
        
        
class PaymentAcceptedUpdateInline(nested_admin.NestedStackedInline):
    model = PaymentAcceptedUpdate
    extra = 0
    can_delete = True
    readonly_fields = ('payment_record','payment_record_payment', )
    fieldsets = (
        (None, {
            'fields': ('payment_record',),
        }),
        (None, {
            'fields': (
                ('payment_record_payment', 'payment',),
            )
        })
    )

    def payment_record_payment(self, obj):
        return obj.payment_record.payment        
        
        

#class ServiceTaxonomyUpdateInline(nested_admin.NestedStackedInline):
#    model = ServiceTaxonomyUpdate
#    extra = 0
#    can_delete = True
#    readonly_fields = ('service_taxonomy_record','service_taxonomy_record_taxonomy','service_taxonomy_record_taxonomy_detail', )
#    fieldsets = (
#        (None, {
#            'fields': ('service_taxonomy_record',)
#        }),
#        (None, {
#            'fields': (
#                ('service_taxonomy_record_taxonomy','taxonomy',),
#                ('service_taxonomy_record_taxonomy_detail','taxonomy_detail',),
#            )
#        })
#    )
#
#    def service_taxonomy_record_taxonomy(self, obj):
#        return obj.service_taxonomy_record.taxonomy
#
#    def service_taxonomy_record_taxonomy_detail(self, obj):
#        return obj.service_taxonomy_record.taxonomy_detail
          


        
class PhysicalAddressUpdateInline(nested_admin.NestedStackedInline):
    model = PhysicalAddressUpdate
    extra = 0
    can_delete = True
    readonly_fields = ('physical_address_record', 'physical_address_record_attention', 'physical_address_record_address_1',
                       'physical_address_record_address_2', 'physical_address_record_address_3', 'physical_address_record_address_4',
                       'physical_address_record_city', 'physical_address_record_region', 'physical_address_record_state_province',
                       'physical_address_record_postal_code', )
    fieldsets = (
        (None, {
            'fields': ('physical_address_record',)
        }),
        (None, {
            'fields': (
                ('physical_address_record_attention', 'attention',),
                ('physical_address_record_address_1', 'address_1',),
                ('physical_address_record_address_2', 'address_2',),
                ('physical_address_record_address_3', 'address_3',),
                ('physical_address_record_address_4', 'address_4',),
                ('physical_address_record_city', 'city',),
                ('physical_address_record_region', 'region',),
                ('physical_address_record_state_province', 'state_province',),
                ('physical_address_record_postal_code', 'postal_code',),
            )
        })
    )

    def physical_address_record_attention(self, obj):
        return obj.physical_address_record.attention

    def physical_address_record_address_1(self, obj):
        return obj.physical_address_record.address_1

    def physical_address_record_address_2(self, obj):
        return obj.physical_address_record.address_2

    def physical_address_record_address_3(self, obj):
        return obj.physical_address_record.address_3

    def physical_address_record_address_4(self, obj):
        return obj.physical_address_record.address_4

    def physical_address_record_city(self, obj):
        return obj.physical_address_record.city

    def physical_address_record_region(self, obj):
        return obj.physical_address_record.region

    def physical_address_record_state_province(self, obj):
        return obj.physical_address_record.get_state_province_display()

    def physical_address_record_postal_code(self, obj):
        return obj.physical_address_record.postal_code


class PhoneUpdateInline(nested_admin.NestedStackedInline):
    form = PhoneUpdateForm
    model = PhoneUpdate
    extra = 0
    can_delete = True
    readonly_fields = ('phone_record_number', 'phone_record_extension', 'phone_record_type', 'phone_record_department', 'phone_record_languages',
                       'phone_record_description', 'phone_record', )
    fieldsets = (
        (None, {
            'fields': ('phone_record',),
        }),
        (None, {
            'fields': (
                ('phone_record_number', 'number', ),
                ('phone_record_extension', 'extension', ),
                ('phone_record_type', 'type', ),
                ('phone_record_department', 'department', ),
                ('phone_record_languages', 'languages', ),
                ('phone_record_description', 'description', )
            )
        })
    )

    def phone_record_number(self, obj):
        return obj.phone_record.number

    def phone_record_extension(self, obj):
        return obj.phone_record.extension

    def phone_record_type(self, obj):
        return obj.phone_record.get_type_display()

    def phone_record_department(self, obj):
        return obj.phone_record.department

    def phone_record_languages(self, obj):
        language_values = []
        for language in obj.phone_record.languages.all():
            language_values.append('(%s) %s' % (language.code, language.name))

        return ", ".join(language_values)

    def phone_record_description(self, obj):
        return obj.phone_record.description

class ContactUpdateInline(nested_admin.NestedStackedInline):
    model = ContactUpdate
    extra = 0
    can_delete = True
    readonly_fields = ('contact_record', 'contact_record_name', 'contact_record_title', 'contact_record_department', 'contact_record_email', )
    fieldsets = (
        (None, {
            'fields': ('contact_record',)
        }),
        (None, {
            'fields': (
                ('contact_record_name', 'name',),
                ('contact_record_title', 'title', ),
                ('contact_record_department', 'department', ),
                ('contact_record_email', 'email', ),
            )
        })
    )

    def contact_record_name(self, obj):
        return obj.contact_record.name

    def contact_record_title(self, obj):
        return obj.contact_record.title

    def contact_record_department(self, obj):
        return obj.contact_record.department

    def contact_record_email(self, obj):
        return obj.contact_record.email

    inlines = [PhoneUpdateInline, ]


class LocationUpdateInline(nested_admin.NestedStackedInline):
    inlines = (PhysicalAddressUpdateInline, ContactUpdateInline,)
    model = LocationUpdate
    extra = 0
    can_delete = True
    readonly_fields = (
        'location_record', 'location_record_name', 'location_record_alternate_name', 'location_record_description', 'location_record_transportation',
        'location_record_latitude', 'location_record_longitude'
    )
    fieldsets = (
        (None, {
            'fields': ('location_record',) ,
        }),
        (None, {
            'fields':
                (
                    ('location_record_name', 'name', ),
                    ('location_record_alternate_name', 'alternate_name', ),
                    ('location_record_description', 'description', ),
                    ('location_record_transportation', 'transportation', ),
                    ('location_record_latitude', 'latitude', ),
                    ('location_record_longitude', 'longitude', ),
                )
        })
    )

    def location_record_name(self, obj):
        return obj.location_record.name

    def location_record_alternate_name(self, obj):
        return obj.location_record.alternate_name

    def location_record_description(self, obj):
        return obj.location_record.description

    def location_record_transportation(self, obj):
        return obj.location_record.transportation

    def location_record_latitude(self, obj):
        return obj.location_record.latitude

    def location_record_longitude(self, obj):
        return obj.location_record.longitude

        
        
        
        
        

class ServiceUpdateAdmin(VersionAdmin, nested_admin.NestedModelAdmin, DefaultFilterMixIn, ListStyleAdminMixin):
    inlines = [EligibilityUpdateInline, PaymentAcceptedUpdateInline, RequiredDocumentUpdateInline, ServiceAreaUpdateInline, LocationUpdateInline, RegularScheduleUpdateInline,HolidayScheduleUpdateInline,]
    change_list_template = 'admin/service/serviceupdate/change_list.html'
    readonly_fields = ('service', 'update_status', 'service_name', 'service_alternate_name', 'service_description', 'service_url','service_email','service_status', 'service_interpretation_services','service_application_process','service_wait_time','service_fees', 'service_accredidations', 'service_licenses', 'service_taxonomy_ids',)
    list_filter = ('update_status', 'service__owner')
    list_display = ('service_owner', 'update_status', 'created', 'name', 'alternate_name', 'description', 'url', 'email', 'status', 'application_process', 'wait_time', 'fees', 'accredidations', 'licenses','validation_note')
    exclude = ('created_by',)
    default_filters = ('update_status__exact=UNPROCESSED',)
    fieldsets = (
        (None, {
            'fields': ('update_status', 'service')
        }),
        (None, {
            'fields':
                (                   
                    ('service_name', 'name',),
                    ('service_alternate_name', 'alternate_name',), 
                    ('service_description', 'description',), 
                    ('service_url', 'url',),
                    ('service_email', 'email',),
                    ('service_status', 'status',),
                    ('service_interpretation_services', 'interpretation_services',),
                    ('service_application_process', 'application_process',),
                    ('service_wait_time', 'wait_time',),
                    ('service_fees', 'fees',), 
                    ('service_accredidations', 'accredidations',),
                    ('service_licenses', 'licenses',),
                    ('service_taxonomy_ids', 'taxonomy_ids',)
                )
        }),
        
        (None, {
            'fields': ('validation_note',)
        }),
    )

    class Media:
        css = { 'all' : ('css/no-addanother-button.css',) }

    def response_change(self, request, obj):
        result = super(ServiceUpdateAdmin, self).response_change(request, obj)
        if "_push_update" in request.POST:

#            """
#            Update Service
#            """

            obj.update_status = ServiceUpdate.STATUS_ACCEPTED
            obj.service.name = obj.name
            obj.service.alternate_name = obj.alternate_name
            obj.service.description = obj.description
            obj.service.url = obj.url
            obj.service.email = obj.email
            obj.service.status = obj.status
            obj.service.interpretation_services = obj.interpretation_services.all()
            obj.service.application_process = obj.application_process
            obj.service.wait_time = obj.wait_time
            obj.service.fees = obj.fees
            obj.service.accredidations = obj.accredidations
            obj.service.licenses = obj.licenses
            obj.service.taxonomy_ids = obj.taxonomy_ids.all()
            obj.service.save()
            obj.save()

            """
            Update Locations
            """
            eligibilities_updates = obj.eligibilities_update.all()
            for eligibility_update in eligibilities_updates:
                if eligibility_update.eligibility_record:
                    eligibility_id = eligibility_update.eligibility_record
                else:
                    eligibility_id = Eligibility()
                    eligibility_id.service = obj.service

                eligibility_id.eligibility_details = eligibility_update.eligibility_details
                eligibility_id.save()
                eligibility_update.save()
            
            
            
            
            payments_updates = obj.payments_update.all()
            for payment_update in payments_updates:
                if payment_update.payment_record:
                    payment_id = payment_update.payment_record
                else:
                    payment_id = PaymentAccepted()
                    payment_id.service = obj.service

                payment_id.payment = payment_update.payment
                payment_id.save()
                payment_update.save()
             


             
            documents_updates = obj.documents_update.all()
            for document_update in documents_updates:
                if document_update.required_document_record:
                    document_id = document_update.required_document_record
                else:
                    document_id = RequiredDocument()
                    document_id.service = obj.service

                document_id.document = document_update.document
                document_id.save()
                document_update.save()

                
                           
            
            
            serviceareas_updates = obj.areas_update.all()
            for servicearea_update in serviceareas_updates:
                if servicearea_update.area_record:
                    servicearea_id = servicearea_update.area_record
                else:
                    servicearea_id = ServiceArea()
                    servicearea_id.service = obj.service

                servicearea_id.description= servicearea_update.description    
                servicearea_id.save()    
                servicearea_id.area= servicearea_update.area.all()
                servicearea_id.save()
                servicearea_update.save()
                
                
            regular_schedule_updates = obj.regular_schedule_updates.all()
            for regular_schedule_update in regular_schedule_updates:
                if regular_schedule_update.regular_schedule_record:
                    regular_schedule_id = regular_schedule_update.regular_schedule_record
                else:
                    regular_schedule_id = RegularSchedule()
                    regular_schedule_id.service = obj.service

                regular_schedule_id.weekday = regular_schedule_update.weekday
                regular_schedule_id.from_hour = regular_schedule_update.from_hour
                regular_schedule_id.to_hour = regular_schedule_update.to_hour
                regular_schedule_id.closed = regular_schedule_update.closed
                regular_schedule_id.save()
                regular_schedule_update.save()  

            holiday_schedule_updates = obj.holiday_schedule_updates.all()
            for holiday_schedule_update in holiday_schedule_updates:
                if holiday_schedule_update.holiday_schedule_record:
                    holiday_schedule_id = holiday_schedule_update.holiday_schedule_record
                else:
                    holiday_schedule_id = HolidaySchedule()
                    holiday_schedule_id.service = obj.service

                holiday_schedule_id.day = holiday_schedule_update.day
                holiday_schedule_id.from_hour = holiday_schedule_update.from_hour
                holiday_schedule_id.to_hour = holiday_schedule_update.to_hour
                holiday_schedule_id.closed = holiday_schedule_update.closed
                holiday_schedule_id.save()
                holiday_schedule_update.save()                 
                

                
                
                
            locations_updates = obj.locations_update.all()
            for location_update in locations_updates:
                if location_update.location_record:
                    location_id = location_update.location_record
                else:
                    location_id = Location()
                    location_id.service = obj.service

                location_id.name = location_update.name
                location_id.alternate_name = location_update.alternate_name
                location_id.description = location_update.description
                location_id.transportation = location_update.transportation
                location_id.latitude = location_update.latitude
                location_id.longitude = location_update.longitude
                location_id.save()
                location_update.save()

                self.update_physical_contacts_for_location(location_update, location_id)
                self.update_contacts_for_location(location_update, location_id)
                


        if "_reject_update" in request.POST:
            obj.update_status = ServiceUpdate.STATUS_REJECTED
            obj.save()

        return result

        
        
    def update_contacts_for_location(self, locations_update, location_record):
        for contact_update in locations_update.contacts_update.all():
            if contact_update.contact_record:
                contact_id = contact_update.contact_record
            else:
                contact_id = Contact()
                contact_id.location = location_record
            contact_id.name = contact_update.name
            contact_id.title = contact_update.title
            contact_id.department = contact_update.department
            contact_id.email = contact_update.email
            contact_id.save()
            contact_update.save()
            self.update_phones_for_contact(contact_update, contact_id)

    def update_phones_for_contact(self, contacts_update, contact_record):
        for phone_update in contacts_update.phones_update.all():
            if phone_update.phone_record:
                phone_id = phone_update.phone_record
            else:
                phone_id = Phone()
                phone_id.contact = contact_record
            phone_id.number = phone_update.number
            phone_id.extension = phone_update.extension
            phone_id.type = phone_update.type
            phone_id.department = phone_update.department
            phone_id.description = phone_update.description
            phone_id.save()
            phone_id.languages = phone_update.languages.all()
            phone_id.save()
            phone_update.save()

    def update_physical_contacts_for_location(self, locations_update, location_record):
        for physical_address_update in locations_update.physical_addresses_update.all():
            if physical_address_update.physical_address_record:
                physical_address_id = physical_address_update.physical_address_record
            else:
                physical_address_id = PhysicalAddress()
                physical_address_id.location = location_record

            physical_address_id.attention = physical_address_update.attention
            physical_address_id.address_1 = physical_address_update.address_1
            physical_address_id.address_2 = physical_address_update.address_2
            physical_address_id.address_3 = physical_address_update.address_3
            physical_address_id.address_4 = physical_address_update.address_4
            physical_address_id.city = physical_address_update.city
            physical_address_id.region = physical_address_update.region
            physical_address_id.state_province = physical_address_update.state_province
            physical_address_id.postal_code = physical_address_update.postal_code
            physical_address_id.save()
            physical_address_update.save()
    
        
        
        
        
        
    def service_name(self, obj):
        return obj.service.name

    def service_alternate_name(self, obj):
        return obj.service.alternate_name

    def service_description(self, obj):
        return obj.service.description

    def service_url(self, obj):
        return obj.service.url

    def service_email(self, obj):
        return obj.service.email

    def service_status(self, obj):
        return obj.service.status
    
    def service_interpretation_services(self, obj):
        language_values = []
        for language in obj.service.interpretation_services.all():
            language_values.append('(%s) %s' % (language.code, language.name))

        return ", ".join(language_values)
    
    def service_application_process(self, obj):
        return obj.service.application_process

    def service_wait_time(self, obj):
        return obj.service.wait_time

    def service_fees(self, obj):
        return obj.service.fees
    
    def service_accredidations(self, obj):
        return obj.service.accredidations
        
    def service_licenses(self, obj):
        return obj.service.licenses
    
    def service_taxonomy_ids(self, obj):
        return ", ".join(obj.service.taxonomy_ids.all().values_list('name', flat=True))
            
    def service_owner(self, obj):
        return obj.service.owner
        
    def get_row_css(self, obj, index):
        return 'status_%s' % obj.update_status
        



#"""
#Main Forms
#""" 



class PaymentAcceptedInline(nested_admin.NestedStackedInline):
    model = PaymentAccepted
    extra = 0
    can_delete = True
    
class RequiredDocumentInline(nested_admin.NestedStackedInline):
    model = RequiredDocument
    extra = 0
    can_delete = True
    
class ServiceAreaInline(nested_admin.NestedStackedInline):
    model = ServiceArea
    extra = 0
    can_delete = True

class EligibilityInline(nested_admin.NestedStackedInline):
    model = Eligibility
    extra = 0
    can_delete = True
    
#class ServiceTaxonomyInline(nested_admin.NestedStackedInline):
#    model = ServiceTaxonomy
#    extra = 0
#    can_delete = True
    
class PhysicalAddressInline(nested_admin.NestedStackedInline):
    model = PhysicalAddress
    extra = 0
    can_delete = True
    


class PhoneInline(nested_admin.NestedStackedInline):
    form = PhoneForm
    model = Phone
    extra = 0
    can_delete = True

class ContactInline(nested_admin.NestedStackedInline):
    model = Contact
    extra = 0
    inlines = [PhoneInline, ]
    can_delete = True


class LocationInline(nested_admin.NestedStackedInline):
    model = Location
    extra = 0
    inlines = [PhysicalAddressInline, ContactInline, ]
    can_delete = True

  
class RegularScheduleInline(nested_admin.NestedTabularInline):
	model = RegularSchedule
	extra = 0
	can_delete = True
    
class HolidayScheduleInline(nested_admin.NestedTabularInline):
	model = HolidaySchedule
	extra = 0
	can_delete = True    
  


class ServiceAdmin(VersionAdmin, nested_admin.NestedModelAdmin):
    inlines = [RegularScheduleInline, HolidayScheduleInline, EligibilityInline, PaymentAcceptedInline, RequiredDocumentInline, ServiceAreaInline, LocationInline]
    list_display = ('name', 'alternate_name', 'description', 'url', 'email', 'status',
        'application_process', 'wait_time', 'fees', 'accredidations', 'licenses')
    search_fields = ('name',)
    exclude = ('created_by', )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()
        
class OrganizationAdmin(VersionAdmin, nested_admin.NestedModelAdmin):
    list_display = ('name', 'alternate_name', 'description', 'url', 'email', 'tax_status',
        'tax_id','year_incorporated','legal_status',)
    search_fields = ('name',) 


admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceUpdate, ServiceUpdateAdmin)
admin.site.register(Organization, OrganizationAdmin)
