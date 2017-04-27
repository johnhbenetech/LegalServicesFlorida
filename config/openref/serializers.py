from .models import Provider, ProviderUpdate
from rest_framework import serializers
 
 
class ProviderUpdateSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = ProviderUpdate
        fields = ('id', 'name', 'description', 'price', 'created_by', 'created', 'status') 

class ProviderSerializer(serializers.ModelSerializer):
    updates = ProviderUpdateSerializer(many=True, read_only=True)
    created_by = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Provider
        fields = ('id','name', 'description', 'price', 'created_by', 'created', 'modified', 'updates')