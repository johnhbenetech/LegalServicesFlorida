from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import Provider, ProviderUpdate
from liststyle import ListStyleAdminMixin


admin.site.site_header = 'My administration'
admin.site.site_title= 'Admin'
admin.site.index_title= 'Admin Actions'


class ProviderUpdateAdmin(VersionAdmin, admin.ModelAdmin, ListStyleAdminMixin):
    readonly_fields = (
        'provider', 'status', 'provider_name', 'provider_phone', 'provider_address', 'provider_description',
        'provider_price',)
    list_filter = ('status', 'provider__owner')
    list_display = ('provider_owner', 'created', 'name', 'phone', 'address', 'description', 'price', 'status',)
    exclude = ('created_by',)

    fieldsets = (
        (None, {
            'fields': ('status', 'provider')
        }),
        (None, {
            'fields':
                (
                    ('provider_name', 'name',),
                    ('provider_phone', 'phone'),
                    ('provider_address', 'address',),
                    ('provider_description', 'description',),
                    ('provider_price', 'price',)
                )
        }),
    )

    def response_change(self, request, obj):
        result = super(ProviderUpdateAdmin, self).response_change(request, obj)
        if "_push_update" in request.POST:
            obj.status = ProviderUpdate.STATUS_ACCEPTED
            obj.provider.name = obj.name
            obj.provider.phone = obj.phone
            obj.provider.address = obj.address
            obj.provider.description = obj.description
            obj.provider.price = obj.price
            obj.provider.save()
            obj.save()

        if "_reject_update" in request.POST:
            obj.status = ProviderUpdate.STATUS_REJECTED
            obj.save()

        return result

    def provider_name(self, obj):
        return obj.provider.name

    def provider_phone(self, obj):
        return obj.provider.phone

    def provider_address(self, obj):
        return obj.provider.address

    def provider_description(self, obj):
        return obj.provider.description

    def provider_price(self, obj):
        return obj.provider.price

    def provider_owner(self, obj):
        return obj.provider.owner

    def get_row_css(self, obj, index):
        return 'status_%s' % obj.status


class ProviderAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('name', 'phone', 'address', 'description', 'price')
    list_filter = ('price',)
    search_fields = ('name', 'price')
    exclude = ('created_by',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()

class PersonAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Provider, ProviderAdmin)
admin.site.register(ProviderUpdate, ProviderUpdateAdmin)
