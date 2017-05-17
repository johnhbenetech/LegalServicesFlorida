from django.views import generic
from .models import Contact, ContactUpdate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.views import login as contrib_login

def login(request):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
    return contrib_login(request)

class ContactUpdateFormView(LoginRequiredMixin, generic.CreateView):
    model = ContactUpdate

    fields = ['contact', 'name', 'phone', 'address', 'description', 'price', ]

    def get_form(self, form_class=None):
        form = super(generic.CreateView, self).get_form(form_class)
        form.fields['contact'].queryset = Contact.objects.filter(owner = self.request.user)

        contact_id = self.request.GET.get('contact_id', False)

        if contact_id:
            contact = Contact.objects.get(pk=contact_id)
            form.fields['contact'].initial = contact.id
            form.fields['name'].initial = contact.name
            form.fields['phone'].initial = contact.phone
            form.fields['address'].initial = contact.address
            form.fields['description'].initial = contact.description
            form.fields['price'].initial = contact.price

        return form

    def get(self, request):
        result = super(generic.CreateView, self).get(request)

        contacts = Contact.objects.filter(owner = self.request.user)
        contact_id = request.GET.get('contact_id', False)

        if contacts.count() == 1 and not contact_id:
            contact = contacts[0]
            return HttpResponseRedirect('%s?contact_id=%s' % (reverse('contact:update'), contact.id))

        return result


class ContactUpdateResultView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'contact/contactupdate_form_result.html'
