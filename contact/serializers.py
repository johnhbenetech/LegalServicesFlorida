from .models import Contact, ContactUpdate
from rest_framework import serializers


class ContactUpdateSerializer(serializers.ModelSerializer):
    def validate_contact(self, contact):
        user = self.context['request'].user
        if contact.owner != user:
            raise serializers.ValidationError("User must be an owner of a Contact")
        return contact

    class Meta:
        model = ContactUpdate
        fields = ('id', 'contact', 'name', 'phone', 'address', 'description', 'price', )


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'name', 'phone', 'address', 'description', 'price', 'created_by', 'created', 'modified', 'owner',)