from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import Provider, ProviderUpdate


admin.site.site_header = 'My administration'
admin.site.site_title= 'Admin'
admin.site.index_title= 'Admin Actions'




class ProviderUpdateAdmin(VersionAdmin, admin.ModelAdmin): 
    list_display = ('name','description','price')
    exclude = ('created_by',)    
    
    def get_queryset(self,request):
        qs = super(ProviderUpdateAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Now we just add an extra filter on the queryset and
        # we're done. Assumption: Page.owner is a foreignkey
        # to a User.
        return qs.filter(provider__owner=request.user)
            
    def formfield_for_foreignkey(self,db_field, request, **kwargs):
        if db_field.name == 'provider':
            if not request.user.is_superuser:
                kwargs["queryset"] = Provider.objects.filter(
                    owner=request.user)
                kwargs['initial'] = 1
        return super(ProviderUpdateAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)   
            
    def save_model(self, request, obj, form, change):
        if not change:
            # the object is being created, so set the user
            obj.created_by = request.user
        obj.save()
        
    
admin.site.register(ProviderUpdate,ProviderUpdateAdmin)

class ProviderAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('name','price','owner')
    list_filter = ('price',)
    search_fields = ('name','price')
    exclude = ('created_by',)

    def get_queryset(self,request):
        qs = super(ProviderAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Now we just add an extra filter on the queryset and
        # we're done. Assumption: Page.owner is a foreignkey
        # to a User.
        return qs.filter(owner=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:
            # the object is being created, so set the user
            obj.created_by = request.user
        obj.save()
	
	
admin.site.register(Provider,ProviderAdmin)