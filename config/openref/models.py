from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Provider(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20)
    created_by = models.ForeignKey(User, related_name='provider_creator')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name='provider_owner')
    def __str__(self):
        return '%s %s' % (self.name, self.price)

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
    provider = models.ForeignKey(Provider, related_name='updates',default=1)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20)
    created_by = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
