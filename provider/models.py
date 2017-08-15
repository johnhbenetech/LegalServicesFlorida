from __future__ import unicode_literals

import select2.fields
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator


STATE_PROVINCE_CHOICES = (('AL', 'Alabama'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'),('AK', 'Alaska'), ('HI', 'Hawaii'))
PHONE_TYPE_CHOICES = (('fixed', 'Fixed'), ('cell', 'Cellular'))


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


class Provider(models.Model):
    organization_name = models.CharField(max_length=255,verbose_name="Organization Name")
    phone = models.CharField(max_length=255, validators=[
            RegexValidator(
                regex='^\([0-9][0-9][0-9]\)[0-9][0-9][0-9]\-[0-9][0-9][0-9][0-9]$',
                message='Phone format must be (555)555-5555',
            ),
        ])
    primary_address = models.TextField(verbose_name="Primary Address",null=True)
    website_url = models.CharField(max_length=255,verbose_name="Website URL",null=True)
    description = models.TextField()
    counties = select2.fields.ManyToManyField(County)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    created_by = models.ForeignKey(User, related_name='provider_creator',blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name='provider_owner',blank=False)

    def __str__(self):
        return '%s, %s, %s, %s, %s' % (self.organization_name, self.phone, self.primary_address, self.description, self.price)


class Location(models.Model):
    provider = models.ForeignKey(Provider, related_name='locations')
    name = models.CharField(max_length=255)
    alternate_name = models.CharField(max_length=255)
    description = models.TextField()
    transportation = models.TextField()
    latitude = models.CharField(max_length=255)
    longtitude = models.CharField(max_length=255)


class Contact(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    email = models.EmailField()
    location = models.ForeignKey(Location,null=True,related_name='contacts')


class Phone(models.Model):
    number = models.CharField(max_length=255, validators=[
            RegexValidator(
                regex='^\([0-9][0-9][0-9]\)[0-9][0-9][0-9]\-[0-9][0-9][0-9][0-9]$',
                message='Phone format must be (555)555-5555',
            ),
        ])
    extension = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=PHONE_TYPE_CHOICES)
    department = models.CharField(max_length=255)
    languages = select2.fields.ManyToManyField(Language, ajax=True,
                                               search_field=lambda q: Q(code__icontains=q) | Q(name__icontains=q))
    description = models.TextField()
    contact = models.ForeignKey(Contact, null=True,related_name='phones')


class PhysicalAddress(models.Model):
    location = models.OneToOneField(Location, related_name='physical_address')
    attention = models.CharField(max_length=255)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    address_3 = models.CharField(max_length=255, blank=True)
    address_4 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=255, blank=True)
    state_province = models.CharField(max_length=2,choices=STATE_PROVINCE_CHOICES,null=True)
    postal_code = models.CharField(max_length=255, blank=True)

#class ContactPerson(models.Model):
#    full_name = models.CharField(max_length=30)
#    email = models.CharField(max_length=30)
#    department = models.CharField(max_length=30)
#    title = models.CharField(max_length=30)
#    phone = models.CharField(max_length=30)
#    provider = models.ForeignKey(Provider, related_name='providercontact',null=True)   


class ProviderUpdate(models.Model):
    STATUS_ACCEPTED = 'ACCEPTED'
    STATUS_REJECTED = 'REJECTED'
    STATUS_NONE = 'UNPROCESSED'
    STATUS_CHOICES = (
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_NONE, 'Unprocessed'),
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_NONE,
    )

    provider = models.ForeignKey(Provider, related_name='provider_update',blank=False,null=False)
    organization_name = models.CharField(max_length=255,verbose_name="Organization Name")
    phone = models.CharField(max_length=255, validators=[
            RegexValidator(
                regex='^\([0-9][0-9][0-9]\)[0-9][0-9][0-9]\-[0-9][0-9][0-9][0-9]$',
                message='Phone format must be (555)555-5555',
            ),
        ])
    primary_address = models.TextField(verbose_name="Primary Address",null=True)
    website_url = models.CharField(max_length=255,verbose_name="Website URL",null=True)
    description = models.TextField()
    counties = select2.fields.ManyToManyField(County)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_emailed = models.BooleanField(default=True)

    def __str__(self):
        return '%s %s' % (self.organization_name, self.phone)

    class Meta:
        ordering = ['-created']


class LocationUpdate(models.Model):
    provider_update = models.ForeignKey(ProviderUpdate,related_name='location_updates')
    location = models.ForeignKey(Location, null=True, blank=True)
    name = models.CharField(max_length=255)
    alternate_name = models.CharField(max_length=255)
    description = models.TextField()
    transportation = models.TextField()
    latitude = models.CharField(max_length=255)
    longtitude = models.CharField(max_length=255)


class PhysicalAddressUpdate(models.Model):
    physical_address = models.ForeignKey(PhysicalAddress,null=True,blank=True)
    attention = models.CharField(max_length=255)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    address_3 = models.CharField(max_length=255, blank=True)
    address_4 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=255, blank=True)
    state_province = models.CharField(max_length=2,choices=STATE_PROVINCE_CHOICES,null=True)
    postal_code = models.CharField(max_length=255, blank=True)
    location_update = models.OneToOneField(LocationUpdate, null=True, related_name='physical_address_update')


class ContactUpdate(models.Model):
    contact = models.ForeignKey(Contact, null=True, blank=True)
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    email = models.EmailField()
    location_update = models.ForeignKey(LocationUpdate,null=True,related_name='contact_updates')


class PhoneUpdate(models.Model):
    phone = models.ForeignKey(Phone, null=True, blank=True)
    number = models.CharField(max_length=255, validators=[
            RegexValidator(
                regex='^\([0-9][0-9][0-9]\)[0-9][0-9][0-9]\-[0-9][0-9][0-9][0-9]$',
                message='Phone format must be (555)555-5555',
            ),
        ])
    extension = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=PHONE_TYPE_CHOICES)
    department = models.CharField(max_length=255)
    languages = select2.fields.ManyToManyField(Language, ajax=True,
                                               search_field=lambda q: Q(code__icontains=q) | Q(name__icontains=q))
    description = models.TextField()
    contact_update = models.ForeignKey(ContactUpdate, null=True,related_name='phone_updates')


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        token = Token.objects.get_or_create(user=instance)[0]


post_save.connect(create_user_profile, sender=User)