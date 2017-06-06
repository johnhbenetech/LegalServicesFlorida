from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import Provider, ProviderUpdate
from liststyle import ListStyleAdminMixin
from django.core.urlresolvers import reverse

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

class ProviderUpdateAdmin(VersionAdmin, DefaultFilterMixIn, ListStyleAdminMixin):
    change_list_template = 'admin/provider/providerupdate/change_list.html'
    readonly_fields = (
        'provider', 'status', 'provider_organization_name', 'provider_phone', 'provider_primary_address', 'provider_description',
        'provider_price','provider_website_url','provider_counties',)
    list_filter = ('status', 'provider__owner')
    list_display = ('provider_owner', 'created', 'organization_name', 'phone', 'primary_address', 'description', 'price', 'status','website_url','counties')
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
        
    def response_change(self, request, obj):
        result = super(ProviderUpdateAdmin, self).response_change(request, obj)
        if "_push_update" in request.POST:
            obj.status = ProviderUpdate.STATUS_ACCEPTED
            obj.provider.organization_name = obj.organization_name
            obj.provider.phone = obj.phone
            obj.provider.primary_address = obj.primary_address
            obj.provider.description = obj.description
            obj.provider.price = obj.price
            obj.provider.website_url = obj.website_url
            obj.provider.counties = obj.counties
            obj.provider.save()
            obj.save()

        if "_reject_update" in request.POST:
            obj.status = ProviderUpdate.STATUS_REJECTED
            obj.save()

        return result

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
        return obj.provider.counties
        
    def get_row_css(self, obj, index):
        return 'status_%s' % obj.status

        
#class ContactAdmin(admin.TabularInline):
#     model = ContactPerson   
#     extra = 0     
 

class ProviderAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('organization_name', 'phone', 'primary_address', 'description', 'price','website_url','counties')
    search_fields = ('organization_name',)
    exclude = ('created_by',)
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()

admin.site.register(Provider, ProviderAdmin)
admin.site.register(ProviderUpdate, ProviderUpdateAdmin)
