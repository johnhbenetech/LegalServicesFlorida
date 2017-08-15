import nested_admin
from django import forms
from django.contrib import admin
from django.core.urlresolvers import reverse
from reversion.admin import VersionAdmin
from .forms import PhoneUpdateForm, PhoneForm

from liststyle import ListStyleAdminMixin
from .models import Provider, ProviderUpdate, Location, PhysicalAddress, Contact, Phone, LocationUpdate, ContactUpdate,\
    PhysicalAddressUpdate, PhoneUpdate


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


class PhysicalAddressUpdateInline(nested_admin.NestedStackedInline):
    model = PhysicalAddressUpdate
    extra = 0
    can_delete = False
    readonly_fields = ('physical_address', 'physical_address_attention', 'physical_address_address_1',
                       'physical_address_address_2', 'physical_address_address_3', 'physical_address_address_4',
                       'physical_address_city', 'physical_address_region', 'physical_address_state_province',
                       'physical_address_postal_code', )
    fieldsets = (
        (None, {
            'fields': ('physical_address',)
        }),
        (None, {
            'fields': (
                ('physical_address_attention', 'attention',),
                ('physical_address_address_1', 'address_1',),
                ('physical_address_address_2', 'address_2',),
                ('physical_address_address_3', 'address_3',),
                ('physical_address_address_4', 'address_4',),
                ('physical_address_city', 'city',),
                ('physical_address_region', 'region',),
                ('physical_address_state_province', 'state_province',),
                ('physical_address_postal_code', 'postal_code',),
            )
        })
    )

    def physical_address_attention(self, obj):
        return obj.physical_address.attention

    def physical_address_address_1(self, obj):
        return obj.physical_address.address_1

    def physical_address_address_2(self, obj):
        return obj.physical_address.address_2

    def physical_address_address_3(self, obj):
        return obj.physical_address.address_3

    def physical_address_address_4(self, obj):
        return obj.physical_address.address_4

    def physical_address_city(self, obj):
        return obj.physical_address.city

    def physical_address_region(self, obj):
        return obj.physical_address.region

    def physical_address_state_province(self, obj):
        return obj.physical_address.get_state_province_display()

    def physical_address_postal_code(self, obj):
        return obj.physical_address.postal_code


class PhoneUpdateInline(nested_admin.NestedStackedInline):
    form = PhoneUpdateForm
    model = PhoneUpdate
    extra = 0
    can_delete = False
    readonly_fields = ('phone_number', 'phone_extension', 'phone_type', 'phone_department', 'phone_languages',
                       'phone_description', 'phone', )
    fieldsets = (
        (None, {
            'fields': ('phone',),
        }),
        (None, {
            'fields': (
                ('phone_number', 'number', ),
                ('phone_extension', 'extension', ),
                ('phone_type', 'type', ),
                ('phone_department', 'department', ),
                ('phone_languages', 'languages', ),
                ('phone_description', 'description', )
            )
        })
    )

    def phone_number(self, obj):
        return obj.phone.number

    def phone_extension(self, obj):
        return obj.phone.extension

    def phone_type(self, obj):
        return obj.phone.get_type_display()

    def phone_department(self, obj):
        return obj.phone.department

    def phone_languages(self, obj):
        language_values = []
        for language in obj.phone.languages.all():
            language_values.append('(%s) %s' % (language.code, language.name))

        return ", ".join(language_values)

    def phone_description(self, obj):
        return obj.phone.description

class ContactUpdateInline(nested_admin.NestedStackedInline):
    model = ContactUpdate
    extra = 0
    can_delete = False
    readonly_fields = ('contact', 'contact_name', 'contact_title', 'contact_department', 'contact_email', )
    fieldsets = (
        (None, {
            'fields': ('contact',)
        }),
        (None, {
            'fields': (
                ('contact_name', 'name',),
                ('contact_title', 'title', ),
                ('contact_department', 'department', ),
                ('contact_email', 'email', ),
            )
        })
    )

    def contact_name(self, obj):
        return obj.contact.name

    def contact_title(self, obj):
        return obj.contact.title

    def contact_department(self, obj):
        return obj.contact.department

    def contact_email(self, obj):
        return obj.contact.email

    inlines = [PhoneUpdateInline, ]


class LocationUpdateInline(nested_admin.NestedStackedInline):
    inlines = (PhysicalAddressUpdateInline, ContactUpdateInline,)
    model = LocationUpdate
    extra = 0
    can_delete = False
    readonly_fields = (
        'location', 'location_name', 'location_alternate_name', 'location_description', 'location_transportation',
        'location_latitude', 'location_longtitude'
    )
    fieldsets = (
        (None, {
            'fields': ('location',) ,
        }),
        (None, {
            'fields':
                (
                    ('location_name', 'name', ),
                    ('location_alternate_name', 'alternate_name', ),
                    ('location_description', 'description', ),
                    ('location_transportation', 'transportation', ),
                    ('location_latitude', 'latitude', ),
                    ('location_longtitude', 'longtitude', ),
                )
        })
    )

    def location_name(self, obj):
        return obj.location.name

    def location_alternate_name(self, obj):
        return obj.location.alternate_name

    def location_description(self, obj):
        return obj.location.description

    def location_transportation(self, obj):
        return obj.location.transportation

    def location_latitude(self, obj):
        return obj.location.latitude

    def location_longtitude(self, obj):
        return obj.location.longtitude


class ProviderUpdateAdmin(VersionAdmin, nested_admin.NestedModelAdmin, DefaultFilterMixIn, ListStyleAdminMixin):
    inlines = (LocationUpdateInline,)
    change_list_template = 'admin/provider/providerupdate/change_list.html'
    readonly_fields = (
        'provider', 'status', 'provider_organization_name', 'provider_phone', 'provider_primary_address', 'provider_description',
        'provider_price','provider_website_url', 'provider_counties')
    list_filter = ('status', 'provider__owner')
    list_display = ('provider_owner', 'created', 'organization_name', 'phone', 'primary_address', 'description', 'price', 'status','website_url')
    exclude = ('created_by',)
    default_filters = ('status__exact=UNPROCESSED',)

    fieldsets = (
        (None, {
            'fields': ('status', 'provider')
        }),
        (None, {
            'fields':
                (
                    ('provider_organization_name', 'organization_name',),
                    ('provider_phone', 'phone'),
                    ('provider_primary_address', 'primary_address',),
                    ('provider_description', 'description',),
                    ('provider_price', 'price',),
                    ('provider_website_url','website_url',),
                    ('provider_counties','counties',)
                )
        }),
    )

    class Media:
        css = { 'all' : ('css/no-addanother-button.css',) }

    def response_change(self, request, obj):
        result = super(ProviderUpdateAdmin, self).response_change(request, obj)
        if "_push_update" in request.POST:
            """
            Update Provider
            """
            obj.status = ProviderUpdate.STATUS_ACCEPTED
            obj.provider.organization_name = obj.organization_name
            obj.provider.phone = obj.phone
            obj.provider.primary_address = obj.primary_address
            obj.provider.description = obj.description
            obj.provider.price = obj.price
            obj.provider.website_url = obj.website_url
            obj.provider.counties = obj.counties.all()
            obj.provider.save()
            obj.save()


            """
            Update Locations
            """
            location_updates = obj.location_updates.all()
            for location_update in location_updates:
                if location_update.location:
                    location = location_update.location
                else:
                    location = Location()
                    location.provider = obj.provider

                location.name = location_update.name
                location.alternate_name = location_update.alternate_name
                location.description = location_update.description
                location.transportation = location_update.transportation
                location.latitude = location_update.latitude
                location.longtitude = location_update.longtitude
                location.save()
                location_update.save()

                self.update_physical_contacts_for_location(location_update, location)
                self.update_contacts_for_location(location_update, location)

        if "_reject_update" in request.POST:
            obj.status = ProviderUpdate.STATUS_REJECTED
            obj.save()

        return result

    def update_contacts_for_location(self, location_update, location):
        for contact_update in location_update.contact_updates.all():
            if contact_update.contact:
                contact = contact_update.contact
            else:
                contact = Contact()
                contact.location = location
            contact.name = contact_update.name
            contact.title = contact_update.title
            contact.department = contact_update.department
            contact.email = contact_update.email
            contact.save()
            contact_update.save()
            self.update_phones_for_contact(contact_update, contact)

    def update_phones_for_contact(self, contact_update, contact):
        for phone_update in contact_update.phone_updates.all():
            if phone_update.phone:
                phone = phone_update.phone
            else:
                phone = Phone()
                phone.contact = contact
            phone.number = phone_update.number
            phone.extension = phone_update.extension
            phone.type = phone_update.type
            phone.department = phone_update.department
            phone.description = phone_update.description
            phone.save()
            phone.languages = phone_update.languages.all()
            phone.save()
            phone_update.save()

    def update_physical_contacts_for_location(self, location_update, location):
        for physical_address_update in [location_update.physical_address_update]:
            if physical_address_update.physical_address:
                physical_address = physical_address_update.physical_address
            else:
                physical_address = PhysicalAddress()
                physical_address.location = location

            physical_address.attention = physical_address_update.attention
            physical_address.address_1 = physical_address_update.address_1
            physical_address.address_2 = physical_address_update.address_2
            physical_address.address_3 = physical_address_update.address_3
            physical_address.address_4 = physical_address_update.address_4
            physical_address.city = physical_address_update.city
            physical_address.region = physical_address_update.region
            physical_address.state_province = physical_address_update.state_province
            physical_address.postal_code = physical_address_update.postal_code
            physical_address.save()
            physical_address_update.save()

    def provider_organization_name(self, obj):
        return obj.provider.organization_name

    def provider_phone(self, obj):
        return obj.provider.phone

    def provider_primary_address(self, obj):
        return obj.provider.primary_address

    def provider_description(self, obj):
        return obj.provider.description

    def provider_price(self, obj):
        return obj.provider.price

    def provider_owner(self, obj):
        return obj.provider.owner
    
    def provider_website_url(self, obj):
        return obj.provider.website_url
    
    def provider_counties(self, obj):
        return ", ".join(obj.provider.counties.all().values_list('name', flat=True))
        
    def get_row_css(self, obj, index):
        return 'status_%s' % obj.status

        
#class ContactAdmin(admin.TabularInline):
#     model = ContactPerson   
#     extra = 0

"""
Main Forms
"""

class PhysicalAddressInline(nested_admin.NestedStackedInline):
    model = PhysicalAddress
    can_delete = False


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


class ProviderAdmin(VersionAdmin, nested_admin.NestedModelAdmin):
    inlines = [LocationInline,]
    list_display = ('organization_name', 'phone', 'primary_address', 'description', 'price', 'website_url',)
    search_fields = ('organization_name',)
    exclude = ('created_by', )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()


admin.site.register(Provider, ProviderAdmin)
admin.site.register(ProviderUpdate, ProviderUpdateAdmin)
