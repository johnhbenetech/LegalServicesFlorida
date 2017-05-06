from django.contrib import admin
from .models import Contact, ContactUpdate
from liststyle import ListStyleAdminMixin


class ContactUpdateAdmin(admin.ModelAdmin, ListStyleAdminMixin):
    readonly_fields = (
        'contact', 'status', 'contact_name', 'contact_phone', 'contact_address', 'contact_description',
        'contact_price',)
    list_filter = ('status', 'contact__owner')
    list_display = ('contact_owner', 'created', 'name', 'phone', 'address', 'description', 'price', 'status',)
    exclude = ('created_by',)

    fieldsets = (
        (None, {
            'fields': ('status', 'contact')
        }),
        (None, {
            'fields':
                (
                    ('contact_name', 'name',),
                    ('contact_phone', 'phone'),
                    ('contact_address', 'address',),
                    ('contact_description', 'description',),
                    ('contact_price', 'price',)
                )
        }),
    )

    def response_change(self, request, obj):
        result = super(ContactUpdateAdmin, self).response_change(request, obj)
        if "_push_update" in request.POST:
            obj.status = ContactUpdate.STATUS_ACCEPTED
            obj.contact.name = obj.name
            obj.contact.phone = obj.phone
            obj.contact.address = obj.address
            obj.contact.description = obj.description
            obj.contact.price = obj.price
            obj.contact.save()
            obj.save()

        if "_reject_update" in request.POST:
            obj.status = ContactUpdate.STATUS_REJECTED
            obj.save()

        return result

    def contact_name(self, obj):
        return obj.contact.name

    def contact_phone(self, obj):
        return obj.contact.phone

    def contact_address(self, obj):
        return obj.contact.address

    def contact_description(self, obj):
        return obj.contact.description

    def contact_price(self, obj):
        return obj.contact.price

    def contact_owner(self, obj):
        return obj.contact.owner

    def get_row_css(self, obj, index):
        return 'status_%s' % obj.status


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address', 'description', 'price')
    list_filter = ('price',)
    search_fields = ('name', 'price')
    exclude = ('created_by',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()


admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactUpdate, ContactUpdateAdmin)
