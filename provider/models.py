from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from multiselectfield import MultiSelectField






class Provider(models.Model):
    COUNTY_CHOICES=(('alachua','Alachua'),('baker','Baker'),('bay','Bay'),('bradford','Bradford'),('brevard','Brevard'),('broward','Broward'),('calhoun','Calhoun'),('charlotte','Charlotte'),('citrus','Citrus'),('clay','Clay'),('collier','Collier'),('columbia','Columbia'),('desoto','DeSoto'),('dixie','Dixie'),('duval','Duval'),('escambia','Escambia'),('flagler','Flagler'),('franklin','Franklin'),('gadsden','Gadsden'),('gilchrist','Gilchrist'),('glades','Glades'),('gulf','Gulf'),('hamilton','Hamilton'),('hardee','Hardee'),('hendry','Hendry'),('hernando','Hernando'),('highlands','Highlands'),('hillsborough','Hillsborough'),('holmes','Holmes'),('indian river','Indian River'),('jackson','Jackson'),('jefferson','Jefferson'),('lafayette','Lafayette'),('lake','Lake'),('lee','Lee'),('leon','Leon'),('levy','Levy'),('liberty','Liberty'),('madison','Madison'),('manatee','Manatee'),('marion','Marion'),('martin','Martin'),('miami-dade','Miami-Dade'),('monroe','Monroe'),('nassau','Nassau'),('okaloosa','Okaloosa'),('okeechobee','Okeechobee'),('orange','Orange'),('osceola','Osceola'),('palm_beach','Palm Beach'),('pasco','Pasco'),('pinellas','Pinellas'),('polk','Polk'),('putnam','Putnam'),('santa_rosa','Santa Rosa'),('sarasota','Sarasota'),('seminole','Seminole'),('st_johns','St. Johns'),('st_lucie','St. Lucie'),('sumter','Sumter'),('suwannee','Suwannee'),('taylor','Taylor'),('union','Union'),('volusia','Volusia'),('wakulla','Wakulla'),('walton','Walton'),('washington','Washington'))
    organization_name = models.CharField(max_length=255,verbose_name="Organization Name")
    phone = models.CharField(max_length=255)
    primary_address = models.TextField(verbose_name="Primary Address",null=True)
    website_url = models.CharField(max_length=255,verbose_name="Website URL",null=True)
    description = models.TextField()
    counties = models.CharField(max_length=255,
        choices=COUNTY_CHOICES, null=True
    )
    price = models.DecimalField(decimal_places=2, max_digits=20)
    created_by = models.ForeignKey(User, related_name='provider_creator',blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name='provider_owner',blank=False)
    
    def __str__(self):
        return '%s, %s, %s, %s, %s' % (self.organization_name, self.phone, self.primary_address, self.description, self.price)



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
    COUNTY_CHOICES=(('alachua','Alachua'),('baker','Baker'),('bay','Bay'),('bradford','Bradford'),('brevard','Brevard'),('broward','Broward'),('calhoun','Calhoun'),('charlotte','Charlotte'),('citrus','Citrus'),('clay','Clay'),('collier','Collier'),('columbia','Columbia'),('desoto','DeSoto'),('dixie','Dixie'),('duval','Duval'),('escambia','Escambia'),('flagler','Flagler'),('franklin','Franklin'),('gadsden','Gadsden'),('gilchrist','Gilchrist'),('glades','Glades'),('gulf','Gulf'),('hamilton','Hamilton'),('hardee','Hardee'),('hendry','Hendry'),('hernando','Hernando'),('highlands','Highlands'),('hillsborough','Hillsborough'),('holmes','Holmes'),('indian river','Indian River'),('jackson','Jackson'),('jefferson','Jefferson'),('lafayette','Lafayette'),('lake','Lake'),('lee','Lee'),('leon','Leon'),('levy','Levy'),('liberty','Liberty'),('madison','Madison'),('manatee','Manatee'),('marion','Marion'),('martin','Martin'),('miami-dade','Miami-Dade'),('monroe','Monroe'),('nassau','Nassau'),('okaloosa','Okaloosa'),('okeechobee','Okeechobee'),('orange','Orange'),('osceola','Osceola'),('palm_beach','Palm Beach'),('pasco','Pasco'),('pinellas','Pinellas'),('polk','Polk'),('putnam','Putnam'),('santa_rosa','Santa Rosa'),('sarasota','Sarasota'),('seminole','Seminole'),('st_johns','St. Johns'),('st_lucie','St. Lucie'),('sumter','Sumter'),('suwannee','Suwannee'),('taylor','Taylor'),('union','Union'),('volusia','Volusia'),('wakulla','Wakulla'),('walton','Walton'),('washington','Washington'))
    organization_name = models.CharField(max_length=255,verbose_name="Organization Name")
    phone = models.CharField(max_length=255)
    primary_address = models.TextField(verbose_name="Primary Address",null=True)
    website_url = models.CharField(max_length=255,verbose_name="Website URL",null=True)
    description = models.TextField()
    counties = models.CharField(max_length=255,
        choices=COUNTY_CHOICES, null=True
    )
    price = models.DecimalField(decimal_places=2, max_digits=20)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' % (self.organization_name, self.phone)

    class Meta:
        ordering = ['-created']

#class ContactPerson(models.Model):
#    full_name = models.CharField(max_length=30)
#    email = models.CharField(max_length=30)
#    department = models.CharField(max_length=30)
#    title = models.CharField(max_length=30)
#    phone = models.CharField(max_length=30)
#    provider = models.ForeignKey(Provider, related_name='providercontact',null=True)   
        