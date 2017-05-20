from rest_framework import viewsets, mixins
from .models import Provider, ProviderUpdate
from .serializers import ProviderSerializer, ProviderUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser


class ProviderList(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProviderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
#        return Provider.objects.filter(owner=self.request.user)
        return Provider.objects.all()

class ProviderUpdateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ProviderUpdateSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)