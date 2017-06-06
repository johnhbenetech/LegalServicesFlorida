import django_tables2 as tables
from .models import ProviderUpdate
from django_tables2.utils import A

class UpdatesTable(tables.Table):
    
    class Meta:
        model = ProviderUpdate
        fields = ('status','primary_address','created','organization_name', 'description', 'price', 'owner')
        attrs = {"class": "table-striped table-bordered"}
        empty_text = "There are no customers matching the search criteria..."