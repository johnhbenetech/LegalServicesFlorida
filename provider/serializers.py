from .models import Provider, ProviderUpdate
from rest_framework import serializers


class ProviderUpdateSerializer(serializers.ModelSerializer):
    def validate_provider(self, provider):
        user = self.context['request'].user
        if provider.owner != user:
            raise serializers.ValidationError("User must be an owner of a Provider")
        return provider

    class Meta:
        model = ProviderUpdate
        fields = ('id', 'provider', 'organization_name', 'phone', 'primary_address', 'description', 'price', 'website_url','counties' )


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ('id', 'organization_name', 'phone', 'primary_address', 'description', 'price', 'website_url','counties', 'created_by', 'created', 'modified', 'owner',)