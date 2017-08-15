from crispy_forms.bootstrap import InlineField, FormActions, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset
from django import forms
from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory

from .models import ProviderUpdate, PhysicalAddressUpdate, LocationUpdate, ContactUpdate, PhoneUpdate, Phone


class UpdateFormHelper(FormHelper):
    form_id = 'update-search-form'
    form_class = 'form-inline'
    field_template = 'bootstrap3/layout/inline_field.html'
    field_class = 'col-xs-3'
    label_class = 'col-xs-3'
    form_show_errors = True
    help_text_inline = False
    html5_required = True
    layout = Layout(
                Fieldset(
                    '<i class="fa fa-search"></i> Search Customer Records',       
                    InlineField('organization_name'),
                    InlineField('description'),
                    InlineField('price'),
                    InlineField('owner'),
                ),
                FormActions(
                    StrictButton(
                        '<i class="fa fa-search"></i> Search', 
                        type='submit',
                        css_class='btn-primary',
                        style='margin-top:10px;')
                )
    )


class BasePhoneUpdateFormset(BaseInlineFormSet):
    @property
    def empty_form(self):
        form = self.form(
            auto_id=self.auto_id,
            prefix=self.add_prefix('__phone_update_prefix__'),
            empty_permitted=True,
            use_required_attribute=False,
            **self.get_form_kwargs(None)
        )
        self.add_fields(form, None)
        return form


class PhoneForm(forms.ModelForm):
    class Meta:
        model=Phone
        fields = ('number', 'extension', 'type', 'department', 'languages', 'description', 'contact', )

    def __init__(self, *args, **kwargs):
        super(PhoneForm, self).__init__(*args, **kwargs)
        self.fields['number'].widget.attrs['class'] = 'phone_number'


class PhoneUpdateForm(forms.ModelForm):
    class Meta:
        model=PhoneUpdate
        fields = ('number', 'extension', 'type', 'department', 'languages', 'description', 'phone',)

    def __init__(self, *args, **kwargs):
        super(PhoneUpdateForm, self).__init__(*args, **kwargs)
        self.fields['number'].widget.attrs['class'] = 'phone_number'

PhoneUpdateFormset = inlineformset_factory(ContactUpdate, PhoneUpdate, extra=0,
                                                     form=PhoneUpdateForm,
                                                     formset=BasePhoneUpdateFormset,
                                                     can_delete=False, can_order=False,
                                                     fields=('number', 'extension', 'type', 'department', 'languages', 'description', 'phone', ),
                                                     widgets={'phone': forms.HiddenInput()})


class BaseContactUpdateFormset(BaseInlineFormSet):
    @property
    def empty_form(self):
        form = self.form(
            auto_id=self.auto_id,
            prefix=self.add_prefix('__contact_update_prefix__'),
            empty_permitted=True,
            use_required_attribute=False,
            **self.get_form_kwargs(None)
        )
        self.add_fields(form, None)
        return form

    def add_fields(self, form, index):
        super(BaseContactUpdateFormset, self).add_fields(form, index)

        form.phone_update = PhoneUpdateFormset(
                        instance=form.instance,
                        data=form.data if form.is_bound else None,
                        files=form.files if form.is_bound else None,
                        prefix='phone_update-%s-%s' % (
                            form.prefix,
                            PhoneUpdateFormset.get_default_prefix()))

    def is_valid(self):
        result = super(BaseContactUpdateFormset, self).is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'phone_update'):
                    result = result and form.phone_update.is_valid()

        return result

    def save(self, commit=True):
        result = super(BaseContactUpdateFormset, self).save(commit=commit)
        for form in self.forms:
            if hasattr(form, 'phone_update'):
                if not self._should_delete_form(form):
                    form.phone_update.save(commit=commit)

        return result


PhysicalAddressUpdateFormset = inlineformset_factory(LocationUpdate, PhysicalAddressUpdate, extra=1,
                              can_delete=0, can_order=0,
                              fields=('physical_address', 'attention', 'address_1', 'address_2', 'address_3', 'address_4',
                                      'city', 'region', 'state_province', 'postal_code', ),
                              widgets={'physical_address': forms.HiddenInput()})


ContactUpdateFormset = inlineformset_factory(LocationUpdate, ContactUpdate, extra=0,
                                                     formset = BaseContactUpdateFormset,
                                                     can_delete=False, can_order=False,
                                                     fields=('contact', 'name', 'title', 'department', 'email',),
                                                     widgets={'contact': forms.HiddenInput()})


class BaseLocationUpdateFormset(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(BaseLocationUpdateFormset, self).add_fields(form, index)

        form.contact_update = ContactUpdateFormset(
                        instance=form.instance,
                        data=form.data if form.is_bound else None,
                        files=form.files if form.is_bound else None,
                        prefix='contact_update-%s-%s' % (
                            form.prefix,
                            ContactUpdateFormset.get_default_prefix()))

        form.physical_address_update = PhysicalAddressUpdateFormset(
                        instance=form.instance,
                        data = form.data if form.is_bound else None,
                        files=form.files if form.is_bound else None,
                        prefix='physical_address_update-%s-%s' % (
                            form.prefix,
                            PhysicalAddressUpdateFormset.get_default_prefix()))

    def is_valid(self):
        result = super(BaseLocationUpdateFormset, self).is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'contact_update'):
                    result = result and form.contact_update.is_valid()
                if hasattr(form, 'physical_address_update'):
                    result = result and form.physical_address_update.is_valid()

        return result

    def save(self, commit=True):
        result = super(BaseLocationUpdateFormset, self).save(commit=commit)
        for form in self.forms:
            if hasattr(form, 'contact_update'):
                if not self._should_delete_form(form):
                    form.contact_update.save(commit=commit)
            if hasattr(form, 'physical_address_update'):
                if not self._should_delete_form(form):
                    form.physical_address_update.save(commit=commit)

        return result


class ProviderUpdateForm(forms.ModelForm):
    class Meta:
        model = ProviderUpdate
        fields = ['provider', 'organization_name', 'phone','website_url', 'primary_address', 'description', 'price', 'counties', ]