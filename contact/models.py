from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20)
    created_by = models.ForeignKey(User, related_name='contact_creator',blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name='contact_owner',blank=False)

    def __str__(self):
        return '%s, %s, %s, %s, %s' % (self.name, self.phone, self.address, self.description, self.price)


class ContactUpdate(models.Model):
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

    contact = models.ForeignKey(Contact, related_name='contact_update',blank=False,null=False)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' % (self.name, self.phone)

    class Meta:
        ordering = ['-created']