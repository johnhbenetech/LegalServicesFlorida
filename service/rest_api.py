from rest_framework import viewsets, mixins
from .models import Service, ServiceUpdate, Organization
from .serializers import ServiceSerializer, ServiceUpdateSerializer, OrganizationSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser


class ServiceList(viewsets.ReadOnlyModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
#        return Provider.objects.filter(owner=self.request.user)
#        queryset = Service.objects.all()
        queryset = Service.objects.filter(owner=self.request.user)
        organizationid = self.request.query_params.get('organizationid',None)
        if organizationid is not None:
            queryset = queryset.filter(organization=organizationid)
        return queryset

class ServiceUpdateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ServiceUpdateSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)
    
    
class OrganizationList(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrganizationSerializer
    permission_classes = (AllowAny,)   

    def get_queryset(self):
        return Organization.objects.all()
    