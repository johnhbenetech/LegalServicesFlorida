import django_tables2 as tables
from .models import ProviderUpdate

class UpdatesTable(tables.Table):
    
    class Meta:
        model = ProviderUpdate
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}