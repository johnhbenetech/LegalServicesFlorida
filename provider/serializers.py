from .models import Provider, Location, PhysicalAddress, Contact, Phone, \
                    ProviderUpdate, LocationUpdate, PhysicalAddressUpdate, ContactUpdate, PhoneUpdate
from rest_framework import serializers

"""
Main Data serializers
"""


class PhysicalAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalAddress
        fields = ('id', 'attention', 'address_1', 'address_2', 'address_3', 'address_4', 'city', 'region',
                  'state_province', 'postal_code',)


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ('id', 'number', 'extension', 'type', 'department', 'languages', 'description', 'contact',)


class ContactSerializer(serializers.ModelSerializer):
    phones = PhoneSerializer(many=True, read_only=True)

    class Meta:
        model = Contact
        fields = ('id', 'name', 'title', 'department', 'email', 'phones', )


class LocationSerializer(serializers.ModelSerializer):
    physical_address = PhysicalAddressSerializer(many=False, read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = Location
        fields = ('id', 'name', 'alternate_name', 'description', 'transportation', 'latitude', 'longtitude',
                  'physical_address', 'contacts', )


class ProviderSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True)

    class Meta:
        model = Provider
        fields = ('id', 'organization_name', 'phone', 'primary_address', 'description', 'price', 'website_url',
                  'counties', 'created_by', 'created', 'modified', 'owner', 'locations', )


"""
Update data serializres
"""


class PhysicalAddressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalAddressUpdate
        fields = ('id', 'physical_address', 'attention', 'address_1', 'address_2', 'address_3', 'address_4', 'city', 'region',
                  'state_province', 'postal_code',)


class PhoneUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneUpdate
        fields = ('id', 'phone', 'number', 'extension', 'type', 'department', 'languages', 'description', )


class ContactUpdateSerializer(serializers.ModelSerializer):
    phone_updates = PhoneUpdateSerializer(many=True, read_only=False)

    class Meta:
        model = ContactUpdate
        fields = ('id', 'contact', 'name', 'title', 'department', 'email', 'phone_updates', )


class LocationUpdateSerializer(serializers.ModelSerializer):
    physical_address_update = PhysicalAddressUpdateSerializer(many=False, read_only=False)
    contact_updates = ContactUpdateSerializer(many=True, read_only=False)

    class Meta:
        model = LocationUpdate
        fields = ('id', 'location', 'name', 'alternate_name', 'description', 'transportation', 'latitude', 'longtitude',
                  'physical_address_update',
                  'contact_updates',
                  )


class ProviderUpdateSerializer(serializers.ModelSerializer):
    location_updates = LocationUpdateSerializer(many=True, required=False)

    def validate_provider(self, provider):
        user = self.context['request'].user
        if provider.owner != user:
            raise serializers.ValidationError("User must be an owner of a Provider")
        return provider

    def create(self, validated_data):
        location_updates = validated_data.pop('location_updates', None)

        provider_update_data = validated_data
        counties = provider_update_data['counties']
        del provider_update_data['counties']

        provider_update = ProviderUpdate.objects.create(**provider_update_data)
        provider_update.save()
        provider_update.counties = counties
        provider_update.is_emailed = False
        provider_update.save()

        for location_update in location_updates:
            location_update_serializer = LocationUpdateSerializer(location_update)
            location_update_serializer_data = location_update_serializer.data
            del location_update_serializer_data['physical_address_update']
            del location_update_serializer_data['contact_updates']
            location_update_serializer_data['location'] = Location.objects.get(pk=location_update_serializer_data['location'])
            location_update_obj = LocationUpdate.objects.create(provider_update=provider_update, **location_update_serializer_data)
            location_update_obj.save()

            physical_address_update_serializer = PhysicalAddressUpdateSerializer(location_update['physical_address_update'])
            physical_address_update_serializer_data = physical_address_update_serializer.data
            physical_address_update_serializer_data['physical_address'] = PhysicalAddress.objects.get(pk=physical_address_update_serializer_data['physical_address'])
            physical_address_update_obj = PhysicalAddressUpdate.objects.create(location_update=location_update_obj, **physical_address_update_serializer_data)
            physical_address_update_obj.save()

            contact_updates = location_update['contact_updates']
            for contact_update in contact_updates:
                contact_update_serializer = ContactUpdateSerializer(contact_update)
                contact_update_serializer_data = contact_update_serializer.data
                contact_update_serializer_data['contact'] = Contact.objects.get(pk=contact_update_serializer_data['contact'])
                phone_updates = contact_update.pop('phone_updates')
                del contact_update_serializer_data['phone_updates']
                contact_update_obj = ContactUpdate.objects.create(location_update=location_update_obj,
                                                                                   **contact_update_serializer_data)
                contact_update_obj.save()

                for phone_update in phone_updates:
                    phone_update_serializer = PhoneUpdateSerializer(phone_update)
                    phone_update_serializer_data = phone_update_serializer.data
                    phone_update_serializer_data['phone'] = Phone.objects.get(
                        pk=phone_update_serializer_data['phone'])

                    languages = phone_update_serializer_data['languages']
                    del phone_update_serializer_data['languages']

                    phone_update_obj = PhoneUpdate.objects.create(contact_update=contact_update_obj,
                                                                      **phone_update_serializer_data)
                    phone_update_obj.save()
                    phone_update_obj.languages = languages
                    phone_update_obj.save()

        return provider_update

    class Meta:
        model = ProviderUpdate
        fields = ('id', 'provider', 'organization_name', 'phone', 'primary_address', 'description', 'price',
                  'website_url', 'counties',
                  'location_updates',
                  )