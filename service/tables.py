import django_tables2 as tables
from .models import ServiceUpdate
from django_tables2.utils import A

class UpdatesTable(tables.Table):
    class Meta:
        model = ServiceUpdate
        fields = ('update_status','name','created','validation_note')
        attrs = {"class": "table-bordered"}
        empty_text = "You have not submitted any updates."