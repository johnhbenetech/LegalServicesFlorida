from .models import Organization, Service, PaymentAccepted, RequiredDocument, ServiceArea, Eligibility, Location, PhysicalAddress, Contact, Phone, RegularSchedule,HolidaySchedule,\
                    ServiceUpdate, PaymentAcceptedUpdate, RequiredDocumentUpdate, ServiceAreaUpdate, EligibilityUpdate, LocationUpdate, PhysicalAddressUpdate, ContactUpdate, PhoneUpdate, RegularScheduleUpdate, HolidayScheduleUpdate
from rest_framework import serializers

"""
Main Data serializers
"""

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'alternate_name','description','url','email','tax_status','tax_id','year_incorporated','legal_status')


class PhysicalAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalAddress
        fields = ('id', 'attention', 'address_1', 'address_2', 'address_3', 'address_4', 'city', 'region',
                  'state_province', 'postal_code','country',)


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ('id', 'number', 'extension', 'type', 'department', 'languages', 'description',)


class ContactSerializer(serializers.ModelSerializer):
    phones = PhoneSerializer(many=True, read_only=True)

    class Meta:
        model = Contact
        fields = ('id', 'name', 'title', 'department', 'email', 'phones', )


class LocationSerializer(serializers.ModelSerializer):
    physical_addresses = PhysicalAddressSerializer(many=True, read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = Location
        fields = ('id', 'name', 'alternate_name', 'description', 'transportation', 'latitude', 'longitude',
                  'contacts', 'physical_addresses', )

class PaymentAcceptedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentAccepted
        fields = ('id', 'payment',)


class RequiredDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequiredDocument
        fields = ('id', 'document',)
        
class ServiceAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceArea
        fields = ('id', 'area', 'description',)

class EligibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Eligibility
        fields = ('id', 'eligibility_details',)
        
class RegularScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegularSchedule
        fields = ('id', 'weekday', 'from_hour', 'to_hour', 'closed') 

class HolidayScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HolidaySchedule
        fields = ('id', 'day', 'from_hour', 'to_hour', 'closed')         
        

#class ServiceTaxonomySerializer(serializers.ModelSerializer):
#    class Meta:
#        model = ServiceTaxonomy
#        fields = ('id', 'taxonomy', 'taxonomy_detail',)
     
        

class ServiceSerializer(serializers.ModelSerializer):
    eligibilities = EligibilitySerializer(many=True, read_only=True)
    payments = PaymentAcceptedSerializer(many=True, read_only=True)
    documents = RequiredDocumentSerializer(many=True, read_only=True)
    areas = ServiceAreaSerializer(many=True, read_only=True)
    locations = LocationSerializer(many=True, read_only=True)
    regular_schedule = RegularScheduleSerializer(many=True, read_only=True)
    holiday_schedule = HolidayScheduleSerializer(many=True, read_only=True)
    class Meta:
        model = Service
        fields = ('id', 'organization','name', 'alternate_name', 'description', 'url', 'email', 'status','interpretation_services',
            'application_process', 'wait_time', 'fees', 'accredidations', 'licenses', 'taxonomy_ids', 'created_by',
            'created', 'modified', 'owner', 'eligibilities', 'payments', 'documents', 'areas','regular_schedule','holiday_schedule','locations')


#"""
#Update data serializres
#"""

class PhysicalAddressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalAddressUpdate
        fields = ('id', 'physical_address_record', 'attention', 'address_1', 'address_2', 'address_3', 'address_4', 'city', 'region',
                  'state_province', 'postal_code','country',)


class PhoneUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneUpdate
        fields = ('id', 'phone_record', 'number', 'extension', 'type', 'department', 'languages', 'description', )


class ContactUpdateSerializer(serializers.ModelSerializer):
    phone_updates = PhoneUpdateSerializer(many=True, read_only=False)

    class Meta:
        model = ContactUpdate
        fields = ('id', 'contact_record', 'name', 'title', 'department', 'email', 'phone_updates', )


class LocationUpdateSerializer(serializers.ModelSerializer):
    physical_address_updates = PhysicalAddressUpdateSerializer(many=True, read_only=False)
    contact_updates = ContactUpdateSerializer(many=True, read_only=False)

    class Meta:
        model = LocationUpdate
        fields = ('id', 'location_record', 'name', 'alternate_name', 'description', 'transportation', 'latitude', 'longitude',
                  'physical_address_updates',
                  'contact_updates',
                  )




class PaymentAcceptedUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentAcceptedUpdate
        fields = ('id', 'payment_record', 'payment',)


class RequiredDocumentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequiredDocumentUpdate
        fields = ('id', 'required_document_record','document',)
              
        
class ServiceAreaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceAreaUpdate
        fields = ('id', 'area_record', 'area', 'description',)

class EligibilityUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EligibilityUpdate
        fields = ('id', 'eligibility_record', 'eligibility_details',)
        
class RegularScheduleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegularScheduleUpdate
        fields = ('id', 'regular_schedule_record', 'weekday', 'from_hour', 'to_hour', 'closed')     
        
        
class HolidayScheduleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HolidayScheduleUpdate
        fields = ('id', 'holiday_schedule_record', 'day', 'from_hour', 'to_hour', 'closed')          

#class ServiceTaxonomyUpdateSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = ServiceTaxonomyUpdate
#        fields = ('id', 'service_taxonomy_record', 'taxonomy', 'taxonomy_detail',)
         
        

class ServiceUpdateSerializer(serializers.ModelSerializer):

    eligibilities_updates = EligibilityUpdateSerializer(many=True, required=False)
    payments_updates = PaymentAcceptedUpdateSerializer(many=True, required=False)
    documents_updates = RequiredDocumentUpdateSerializer(many=True, required=False)
    serviceareas_updates = ServiceAreaUpdateSerializer(many=True, required=False)
    locations_updates = LocationUpdateSerializer(many=True, required=False)
    regular_schedule_updates = RegularScheduleUpdateSerializer(many=True, required=False)
    holiday_schedule_updates = HolidayScheduleUpdateSerializer(many=True, required=False)

    def validate_service(self, service):
        user = self.context['request'].user
        if service.owner != user:
            raise serializers.ValidationError("User must be an owner of a Service")
        return service

    def create(self, validated_data):
        eligibilities_updates = validated_data.pop('eligibilities_updates', None)
        payments_updates = validated_data.pop('payments_updates', None)
        documents_updates = validated_data.pop('documents_updates', None)
        serviceareas_updates = validated_data.pop('serviceareas_updates', None)
        locations_updates = validated_data.pop('locations_updates', None)
        regular_schedule_updates = validated_data.pop('regular_schedule_updates', None)
        holiday_schedule_updates = validated_data.pop('holiday_schedule_updates', None)
        
        print(documents_updates)
        print(regular_schedule_updates)
        
        service_update_data = validated_data
        interpretation_services = service_update_data['interpretation_services']
        del service_update_data['interpretation_services']
        
        taxonomy_ids = service_update_data['taxonomy_ids']
        del service_update_data['taxonomy_ids']
        
        

        service_update = ServiceUpdate.objects.create(**service_update_data)
        service_update.save()
        service_update.interpretation_services = interpretation_services
        service_update.taxonomy_ids = taxonomy_ids
        
        service_update.is_emailed = False
        service_update.save()
        
        for eligibility_update in eligibilities_updates:
            eligibility_update_serializer = EligibilityUpdateSerializer(eligibility_update)
            eligibility_update_serializer_data = eligibility_update_serializer.data
            eligibility_update_serializer_data['eligibility_record'] = Eligibility.objects.get(pk=eligibility_update_serializer_data['eligibility_record'])
            eligibility_update_obj = EligibilityUpdate.objects.create(service_update=service_update, **eligibility_update_serializer_data)
            eligibility_update_obj.save()
        
        for payment_update in payments_updates:
            payment_update_serializer = PaymentAcceptedUpdateSerializer(payment_update)
            payment_update_serializer_data = payment_update_serializer.data
            payment_update_serializer_data['payment_record'] = PaymentAccepted.objects.get(pk=payment_update_serializer_data['payment_record'])
            payment_update_obj = PaymentAcceptedUpdate.objects.create(service_update=service_update, **payment_update_serializer_data)
            payment_update_obj.save()
        
        for document_update in documents_updates:
            document_update_serializer = RequiredDocumentUpdateSerializer(document_update)
            document_update_serializer_data = document_update_serializer.data
            document_update_serializer_data['required_document_record'] = RequiredDocument.objects.get(pk=document_update_serializer_data['required_document_record'])
            document_update_obj = RequiredDocumentUpdate.objects.create(service_update=service_update, **document_update_serializer_data)
            document_update_obj.save()  

        for regular_schedule_update in regular_schedule_updates:
            regular_schedule_update_serializer = RegularScheduleUpdateSerializer(regular_schedule_update)
            regular_schedule_update_serializer_data = regular_schedule_update_serializer.data
            regular_schedule_update_serializer_data['regular_schedule_record'] = RegularSchedule.objects.get(pk=regular_schedule_update_serializer_data['regular_schedule_record'])
            regular_schedule_update_obj = RegularScheduleUpdate.objects.create(service_update=service_update, **regular_schedule_update_serializer_data)
            regular_schedule_update_obj.save() 

        for holiday_schedule_update in holiday_schedule_updates:
            holiday_schedule_update_serializer = HolidayScheduleUpdateSerializer(holiday_schedule_update)
            holiday_schedule_update_serializer_data = holiday_schedule_update_serializer.data
            holiday_schedule_update_serializer_data['holiday_schedule_record'] = HolidaySchedule.objects.get(pk=holiday_schedule_update_serializer_data['holiday_schedule_record'])
            holiday_schedule_update_obj = HolidayScheduleUpdate.objects.create(service_update=service_update, **holiday_schedule_update_serializer_data)
            holiday_schedule_update_obj.save()               
            
            
            
        for servicearea_update in serviceareas_updates:
            servicearea_update_serializer = ServiceAreaUpdateSerializer(servicearea_update)
            servicearea_update_serializer_data = servicearea_update_serializer.data
            servicearea_update_serializer_data['area_record'] = ServiceArea.objects.get(pk=servicearea_update_serializer_data['area_record'])
            
            area = servicearea_update_serializer_data['area']
            del servicearea_update_serializer_data['area']
            
            servicearea_update_obj = ServiceAreaUpdate.objects.create(service_update=service_update, **servicearea_update_serializer_data)
            servicearea_update_obj.save()
            servicearea_update_obj.area = area
            servicearea_update_obj.save()

            
        for location_update in locations_updates:
            location_update_serializer = LocationUpdateSerializer(location_update)
            location_update_serializer_data = location_update_serializer.data
            del location_update_serializer_data['physical_address_updates']
            del location_update_serializer_data['contact_updates']
            location_update_serializer_data['location_record'] = Location.objects.get(pk=location_update_serializer_data['location_record'])
            location_update_obj = LocationUpdate.objects.create(service_update=service_update, **location_update_serializer_data)
            location_update_obj.save()


            physical_addresses_updates = location_update['physical_address_updates']
            for physical_address_update in physical_addresses_updates:
                physical_address_update_serializer = PhysicalAddressUpdateSerializer(physical_address_update)
                physical_address_update_serializer_data = physical_address_update_serializer.data
                physical_address_update_serializer_data['physical_address_record'] = PhysicalAddress.objects.get(pk=physical_address_update_serializer_data['physical_address_record'])
                physical_address_update_obj = PhysicalAddressUpdate.objects.create(location_update=location_update_obj,
                                                                                   **physical_address_update_serializer_data)
                physical_address_update_obj.save()            
     
            
            contacts_updates = location_update['contact_updates']
            for contact_update in contacts_updates:
                contact_update_serializer = ContactUpdateSerializer(contact_update)
                contact_update_serializer_data = contact_update_serializer.data
                contact_update_serializer_data['contact_record'] = Contact.objects.get(pk=contact_update_serializer_data['contact_record'])
                phone_updates = contact_update.pop('phone_updates')
                del contact_update_serializer_data['phone_updates']
                contact_update_obj = ContactUpdate.objects.create(location_update=location_update_obj,
                                                                                   **contact_update_serializer_data)
                contact_update_obj.save()

                for phone_update in phone_updates:
                    phone_update_serializer = PhoneUpdateSerializer(phone_update)
                    phone_update_serializer_data = phone_update_serializer.data
                    phone_update_serializer_data['phone_record'] = Phone.objects.get(
                        pk=phone_update_serializer_data['phone_record'])

                    languages = phone_update_serializer_data['languages']
                    del phone_update_serializer_data['languages']

                    phone_update_obj = PhoneUpdate.objects.create(contact_update=contact_update_obj,
                                                                      **phone_update_serializer_data)
                    phone_update_obj.save()
                    phone_update_obj.languages = languages
                    phone_update_obj.save()
             
            
        
        return service_update

    class Meta:
        model = ServiceUpdate
        fields = ('id', 'service', 'name', 'alternate_name', 'description', 'url', 'email', 'status','interpretation_services',
            'application_process', 'wait_time', 'fees', 'accredidations', 'licenses', 'taxonomy_ids', 'validation_note','eligibilities_updates', 'payments_updates', 'documents_updates','serviceareas_updates','regular_schedule_updates','holiday_schedule_updates','locations_updates',)