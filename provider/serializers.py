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
        fields = ('id', 'provider', 'name', 'phone', 'address', 'description', 'price', )


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ('id', 'name', 'phone', 'address', 'description', 'price', 'created_by', 'created', 'modified', 'owner',)