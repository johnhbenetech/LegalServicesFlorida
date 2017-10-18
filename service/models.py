from __future__ import unicode_literals

import select2.fields
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator


STATE_PROVINCE_CHOICES = (('AL', 'Alabama'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'),('AK', 'Alaska'), ('HI', 'Hawaii'))
PHONE_TYPE_CHOICES = (('fixed', 'Fixed'), ('cell', 'Cellular'),('fax','Fax'), ('hotline','Hotline'))


class Language(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=255)

    def __str__(self):
        return "(%s) %s" % (self.code, self.name)


class County(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name
        
class Taxonomy(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name  


class Organization(models.Model):
    name = models.CharField(max_length=255,blank=False)
    alternate_name = models.CharField(max_length=255,blank=True)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=255,verbose_name="Website URL",blank=True)
    email = models.EmailField(blank=True)
    tax_status = models.CharField(max_length=255,blank=True)
    tax_id = models.CharField(max_length=255,blank=True)
    year_incorporated = models.CharField(max_length=255,blank=True)
    legal_status = models.CharField(max_length=255,blank=True)
    def __str__(self):
        return '%s' % (self.name)   
  
        
class Service(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        blank=False,null=True,
        related_name='service_organization'
    )
    name = models.CharField(max_length=255,blank=False)
    alternate_name = models.CharField(max_length=255,blank=True)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=255,verbose_name="Website URL",blank=True)
    email = models.EmailField(blank=True)
    status = models.CharField(max_length=255,blank=True)
    interpretation_services = select2.fields.ManyToManyField(Language,blank=True, ajax=True,
                                               search_field=lambda q: Q(code__icontains=q) | Q(name__icontains=q))
    application_process = models.CharField(max_length=255,blank=True)
    wait_time = models.CharField(max_length=255,blank=True)
    fees = models.CharField(max_length=255,blank=True)
    accredidations = models.CharField(max_length=255,blank=True)
    licenses = models.CharField(max_length=255,blank=True)
    taxonomy_ids = select2.fields.ManyToManyField(Taxonomy,blank=True)
    created_by = models.ForeignKey(User, related_name='service_creator',blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name='service_owner',blank=False)
    def __str__(self):
        return '%s, %s, %s' % (self.name, self.email, self.description)
        
class ServiceUpdate(models.Model):
    STATUS_ACCEPTED = 'ACCEPTED'
    STATUS_REJECTED = 'REJECTED'
    STATUS_NONE = 'UNPROCESSED'
    STATUS_CHOICES = (
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_NONE, 'Unprocessed'),
    )
    update_status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_NONE,
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        blank=False,null=True,
        related_name='service_update_organization'
    )
    service = models.ForeignKey(Service, related_name='service_update',blank=False,null=False)
    name = models.CharField(max_length=255,blank=True)
    alternate_name = models.CharField(max_length=255,blank=True)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=255,verbose_name="Website URL",blank=True)
    email = models.EmailField(blank=True)
    status = models.CharField(max_length=255,blank=True)
    interpretation_services = select2.fields.ManyToManyField(Language,blank=True, ajax=True,
                                               search_field=lambda q: Q(code__icontains=q) | Q(name__icontains=q))
    application_process = models.CharField(max_length=255,blank=True)
    wait_time = models.CharField(max_length=255,blank=True)
    fees = models.CharField(max_length=255,blank=True)
    accredidations = models.CharField(max_length=255,blank=True)
    licenses = models.CharField(max_length=255,blank=True)
    taxonomy_ids = select2.fields.ManyToManyField(Taxonomy,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_emailed = models.BooleanField(default=False)
    validation_note = models.TextField(blank=True)
    def __str__(self):
        return '%s %s' % (self.name, self.description)

    class Meta:
        ordering = ['-created']

        
        
class Location(models.Model):
    service = models.ForeignKey(Service, related_name='locations')
    name = models.CharField(max_length=255,blank=True)
    alternate_name = models.CharField(max_length=255,blank=True)
    description = models.TextField(blank=True)
    transportation = models.TextField(blank=True)
    latitude = models.CharField(max_length=15,blank=True)
    longitude = models.CharField(max_length=15,blank=True)
    
    
class LocationUpdate(models.Model):
    service_update = models.ForeignKey(ServiceUpdate, related_name='locations_update')
    location_record = models.ForeignKey(Location, null=True, blank=True)
    name = models.CharField(max_length=255,blank=True)
    alternate_name = models.CharField(max_length=255,blank=True)
    description = models.TextField(blank=True)
    transportation = models.TextField(blank=True)
    latitude = models.CharField(max_length=15,blank=True)
    longitude = models.CharField(max_length=15,blank=True)
    
    

    
    
class PaymentAccepted(models.Model):
    service = models.ForeignKey(Service, related_name='payments')
    payment = models.TextField(blank=True)
    
class PaymentAcceptedUpdate(models.Model):
    service_update = models.ForeignKey(ServiceUpdate,related_name='payments_update',null=True, blank=True)
    payment_record = models.ForeignKey(PaymentAccepted, null=True, blank=True)
    payment = models.TextField(blank=True)

class RequiredDocument(models.Model):
    service = models.ForeignKey(Service, related_name='documents')
    document = models.TextField(blank=True)
    
class RequiredDocumentUpdate(models.Model):
    service_update = models.ForeignKey(ServiceUpdate,related_name='documents_update',null=True, blank=True)
    required_document_record = models.ForeignKey(RequiredDocument, null=True, blank=True)
    document = models.TextField(blank=True)
    
class ServiceArea(models.Model):
    service = models.ForeignKey(Service, related_name='areas')
    area = select2.fields.ManyToManyField(County,ajax=True,search_field=lambda q: Q(name__icontains=q),blank=True)
    description = models.TextField(blank=True)
    
class ServiceAreaUpdate(models.Model):
    service_update = models.ForeignKey(ServiceUpdate,related_name='areas_update',null=True, blank=True)
    area_record = models.ForeignKey(ServiceArea, null=True, blank=True)
    area = select2.fields.ManyToManyField(County, ajax=True,search_field=lambda q: Q(name__icontains=q),blank=True)
    description = models.TextField(blank=True)
    
    
class Eligibility(models.Model):
    service = models.ForeignKey(Service, related_name='eligibilities')
    eligibility_details = models.TextField(blank=True)
    
class EligibilityUpdate(models.Model):
    service_update = models.ForeignKey(ServiceUpdate,related_name='eligibilities_update',null=True, blank=True)
    eligibility_record = models.ForeignKey(Eligibility,null=True, blank=True)
    eligibility_details = models.TextField(blank=True)
    
#class ServiceTaxonomy(models.Model):
#    service = models.ForeignKey(Service, related_name='taxonomies')
#    taxonomy = select2.fields.ManyToManyField(Taxonomy,blank=True)
#    taxonomy_detail = models.TextField(blank=True)
#    
#class ServiceTaxonomyUpdate(models.Model):
#    service_update = models.ForeignKey(ServiceUpdate, related_name='taxonomies_update',null=True, blank=True)
#    service_taxonomy_record = models.ForeignKey(ServiceTaxonomy, null=True, blank=True)
#    taxonomy = select2.fields.ManyToManyField(Taxonomy,blank=True)
#    taxonomy_detail = models.TextField(blank=True)



WEEKDAYS = [
  (1, ("Sunday")),
  (2, ("Monday")),
  (3, ("Tuesday")),
  (4, ("Wednesday")),
  (5, ("Thursday")),
  (6, ("Friday")),
  (7, ("Saturday")),
]


class RegularSchedule(models.Model):
    service = models.ForeignKey(Service, related_name='regular_schedule')
    weekday = models.IntegerField(choices=WEEKDAYS,blank=True)
    from_hour = models.TimeField(blank=True, null=True)
    to_hour = models.TimeField(blank=True, null=True)
    closed = models.BooleanField(default=False, blank=True)

#    class Meta:
#        ordering = ['weekday']
#
#    def __unicode__(self):
#        return u'%s: %s - %s' % (self.get_weekday_display(),
#                                 self.from_hour, self.to_hour)
                                 
                                 
class RegularScheduleUpdate(models.Model):
    service_update = models.ForeignKey(ServiceUpdate,related_name='regular_schedule_updates',null=True, blank=True)
    regular_schedule_record = models.ForeignKey(RegularSchedule,null=True, blank=True)
    weekday = models.IntegerField(choices=WEEKDAYS,blank=True,null=True)
    from_hour = models.TimeField(blank=True, null=True)
    to_hour = models.TimeField(blank=True, null=True)
    closed = models.BooleanField(default=False, blank=True)

#    class Meta:
#        ordering = ['weekday']
#
#    def __unicode__(self):
#        return u'%s: %s - %s' % (self.get_weekday_display(),
#                                 self.from_hour, self.to_hour)     

class HolidaySchedule(models.Model):
    service = models.ForeignKey(Service, related_name='holiday_schedule')
    day = models.DateField(blank=True,null=True)
    from_hour = models.TimeField(blank=True, null=True)
    to_hour = models.TimeField(blank=True, null=True)
    closed = models.BooleanField(default=False, blank=True)

#    class Meta:
#        ordering = ['day']
#
#    def __unicode__(self):
#        return u'%s: %s - %s' % (self.day,
#                                 self.from_hour, self.to_hour)
                                 
                                 
class HolidayScheduleUpdate(models.Model):
    service_update = models.ForeignKey(ServiceUpdate,related_name='holiday_schedule_updates',null=True, blank=True)
    holiday_schedule_record = models.ForeignKey(HolidaySchedule,null=True, blank=True)
    day = models.DateField(blank=True, null=True)
    from_hour = models.TimeField(blank=True, null=True)
    to_hour = models.TimeField(blank=True, null=True)
    closed = models.BooleanField(default=False,blank=True)

#    class Meta:
#        ordering = ['day']
#
#    def __unicode__(self):
#        return u'%s: %s - %s' % (self.day,
#                                 self.from_hour, self.to_hour)





                                 
   
class Contact(models.Model):
    location = models.ForeignKey(Location,null=True,related_name='contacts')
    name = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)



class Phone(models.Model):
    contact = models.ForeignKey(Contact,related_name='phones')   
    number = models.CharField(max_length=255, blank=True, validators=[
            RegexValidator(
                regex='^\([0-9][0-9][0-9]\)[0-9][0-9][0-9]\-[0-9][0-9][0-9][0-9]$',
                message='Phone format must be (555)555-5555',
            ),
        ])
    extension = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=10, choices=PHONE_TYPE_CHOICES, blank=True)
    department = models.CharField(max_length=255, blank=True)
    languages = select2.fields.ManyToManyField(Language, blank=True, ajax=True,
                                               search_field=lambda q: Q(code__icontains=q) | Q(name__icontains=q))
    description = models.TextField(blank=True)
 
    
class PhysicalAddress(models.Model):
    location = models.ForeignKey(Location, related_name='physical_addresses')
    attention = models.CharField(max_length=255, blank=True)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    address_3 = models.CharField(max_length=255, blank=True)
    address_4 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=255, blank=True)
    state_province = models.CharField(max_length=2,choices=STATE_PROVINCE_CHOICES,null=True, blank=True)
    postal_code = models.CharField(max_length=255, blank=True)   
    country = models.CharField(max_length=2, blank=True)    
    
class PhysicalAddressUpdate(models.Model):
    location_update = models.ForeignKey(LocationUpdate,null=True, related_name='physical_addresses_update')
    physical_address_record = models.ForeignKey(PhysicalAddress,null=True,blank=True)
    attention = models.CharField(max_length=255, blank=True)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    address_3 = models.CharField(max_length=255, blank=True)
    address_4 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=255, blank=True)
    state_province = models.CharField(max_length=2,choices=STATE_PROVINCE_CHOICES, null=True,blank=True)
    postal_code = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=2, blank=True)



class ContactUpdate(models.Model):
    location_update = models.ForeignKey(LocationUpdate,null=True, related_name='contacts_update')
    contact_record = models.ForeignKey(Contact, null=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)



class PhoneUpdate(models.Model):
    contact_update = models.ForeignKey(ContactUpdate, null=True,related_name='phones_update')
    phone_record = models.ForeignKey(Phone, null=True, blank=True)
    number = models.CharField(max_length=255, blank=True, validators=[
            RegexValidator(
                regex='^\([0-9][0-9][0-9]\)[0-9][0-9][0-9]\-[0-9][0-9][0-9][0-9]$',
                message='Phone format must be (555)555-5555',
            ),
        ])
    extension = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=10, choices=PHONE_TYPE_CHOICES, blank=True)
    department = models.CharField(max_length=255, blank=True)
    languages = select2.fields.ManyToManyField(Language, blank=True, ajax=True,
                                               search_field=lambda q: Q(code__icontains=q) | Q(name__icontains=q))
    description = models.TextField(blank=True)

    
   
    
        
    
    
    
    
    
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        token = Token.objects.get_or_create(user=instance)[0]


post_save.connect(create_user_profile, sender=User)