from rest_framework import viewsets, mixins
from .models import Contact, ContactUpdate
from .serializers import ContactSerializer, ContactUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser


class ContactList(viewsets.ReadOnlyModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
#        return Contact.objects.filter(owner=self.request.user)
        return Contact.objects.all()

class ContactUpdateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ContactUpdateSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)