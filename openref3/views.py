from django.views import generic
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.urls import reverse
import os
from django.utils import timezone
from datetime import timedelta
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import get_template
from django.template import Context
from service.models import ServiceUpdate, Service, User


    
def countsubchanges(modelset, recordname, level1, level2=None, level3=None):
    changes = 0
    for model in getattr(modelset,level1).all():       
        if level3:
            for submodel in getattr(model,level2).all():
                for subsubmodel in getattr(submodel,level3).all():
                    parent = getattr(subsubmodel,recordname)
                    if parent:            
                        for field in subsubmodel._meta.get_fields():
                            if (not field.auto_created) and field.many_to_many:
                                if (set(getattr(subsubmodel,field.name).all()) != set(getattr(parent,field.name).all())) and (len(getattr(subsubmodel,field.name).all())+len(getattr(parent,field.name).all())) > 0:
                                    changes+=1                              
                            
                            elif (not field.auto_created) and (not field.is_relation) and (getattr(subsubmodel,field.name) != getattr(parent,field.name)):
                                changes+=1
                    else:
                        for field in subsubmodel._meta.get_fields():
                            if ((not field.auto_created) and (not field.is_relation) and (getattr(subsubmodel,field.name) != "") and (getattr(subsubmodel,field.name) != None)) or field.many_to_many:
                                changes+=1
               
        elif level2:
            for submodel in getattr(model,level2).all():
                parent = getattr(submodel,recordname)
                if parent:            
                    for field in submodel._meta.get_fields():
                        if (not field.auto_created) and field.many_to_many:
                            if (set(getattr(submodel,field.name).all()) != set(getattr(parent,field.name).all())) and (len(getattr(submodel,field.name).all())+len(getattr(parent,field.name).all())) > 0:
                                changes+=1                        
                        
                        elif (not field.auto_created) and (not field.is_relation) and (getattr(submodel,field.name) != getattr(parent,field.name)):
                            changes+=1
                else:
                    for field in submodel._meta.get_fields():
                        if ((not field.auto_created) and (not field.is_relation) and (getattr(submodel,field.name) != "") and (getattr(submodel,field.name) != None)) or field.many_to_many:
                            changes+=1
        
        else:
            parent = getattr(model,recordname)
            if parent:                
                for field in model._meta.get_fields():
                    if (not field.auto_created) and field.many_to_many:
                        if (set(getattr(model,field.name).all()) != set(getattr(parent,field.name).all())) and (len(getattr(model,field.name).all())+len(getattr(parent,field.name).all())) > 0:
                            changes+=1
                    elif (not field.auto_created) and (not field.is_relation) and (getattr(model,field.name) != getattr(parent,field.name)):
                        changes+=1
            else:
                for field in model._meta.get_fields():
                    if ((not field.auto_created) and (not field.is_relation) and (getattr(model,field.name) != "") and (getattr(model,field.name) != None)) or field.many_to_many:
                        changes+=1            

         

                        


    return changes

def countchanges(modelset, recordname):
    changes = 0
    parent = getattr(modelset,recordname)    
    service_fields = [f.name for f in parent._meta.get_fields() if f.name not in ['created','modified']]
    for field in modelset._meta.get_fields():
        if (field.name in service_fields) and (not field.auto_created) and field.many_to_many:
            if (set(getattr(modelset,field.name).all()) != set(getattr(parent,field.name).all())) and (len(getattr(modelset,field.name).all())+len(getattr(parent,field.name).all())) > 0:
                changes+=1
            
        elif (not field.auto_created) and (field.name in service_fields) and (getattr(modelset,field.name) != getattr(parent,field.name)):           
            changes+=1 
    
    return changes



@staff_member_required
def email(request):
    subject = "Weekly Services Updates"
    from_email = 'notifications@accountmail.co'
    to = list(User.objects.filter(groups__name='Update Emails').values_list('email', flat=True))

    service_updates = ServiceUpdate.objects.filter(is_emailed=False,update_status='UNPROCESSED')
    update_count = ServiceUpdate.objects.filter(update_status='UNPROCESSED').count()

    
    week_count = ServiceUpdate.objects.filter(update_status='UNPROCESSED',created__gte=timezone.now()-timedelta(days=7),).count()
    old_count = ServiceUpdate.objects.filter(update_status='UNPROCESSED',created__lte=timezone.now()-timedelta(days=14),).count()
    
    
    for update in service_updates:
        parentid = update.service_id
        serviceobj = Service.objects.filter(id=parentid)[0]   


        totalchanges = countchanges(update,'service') \
        + countsubchanges(update,'physical_address_record','locations_update','physical_addresses_update') \
        + countsubchanges(update,'contact_record','locations_update','contacts_update') \
        + countsubchanges(update,'phone_record','locations_update','contacts_update','phones_update') \
        + countsubchanges(update,'location_record','locations_update') \
        + countsubchanges(update,'payment_record','payments_update') \
        + countsubchanges(update,'required_document_record','documents_update') \
        + countsubchanges(update,'eligibility_record','eligibilities_update',) \
        + countsubchanges(update,'area_record','areas_update',) \
        + countsubchanges(update,'regular_schedule_record','regular_schedule_updates',) \
        + countsubchanges(update,'holiday_schedule_record','holiday_schedule_updates',)
        
        setattr(update, 'totalchanges', totalchanges)
        print(getattr(update,'totalchanges'))
        
    html_template = get_template('service/email/service_updates.html')
    text_template = get_template('service/email/service_updates.txt')
    context = {'service_updates': service_updates, 'update_count': update_count, 'week_count': week_count, 'old_count': old_count,}

    text_content = text_template.render(context)
    html_content = html_template.render(context)

    
    if service_updates:
        connection = get_connection()
        connection.open()
    
        msg = EmailMultiAlternatives(subject, text_content, from_email, bcc=to, connection=connection)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    
    
    return HttpResponseRedirect('/admin/service/serviceupdate/?update_status__exact=UNPROCESSED')