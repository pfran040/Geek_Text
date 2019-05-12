from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Address, CreditCard
from crispy_forms.helper import FormHelper

import datetime
import re
from django.core.exceptions import ValidationError
from django.forms import ModelForm, ChoiceField, CharField
from users.payments import MONTHS, YEARS

# User registration form
class UserSignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Form to update username and email at the profile
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

# Form to upload new profile picture
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

# Form to update first name and last name
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

# Form to upddate the user bio at the profile page
class BioForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']

    def __init__(self, *args, **kwargs):
        super(BioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class NicknameForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nick_name']

    def __init__(self, *args, **kwargs):
        super(NicknameForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class EditAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'address1', 'address2', 'city', 'state', 'zipcode', 'primaryAddress']

    def __init__(self, *args, **kwargs):
        super(EditAddressForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

        self.fields['name'].required = True
        self.fields['address1'].required = True
        self.fields['city'].required = True
        self.fields['state'].required = True
        self.fields['zipcode'].required = True

        self.fields['name'].widget.attrs[
            'placeholder'] = 'Shipping address familiar name'
        self.fields['address1'].widget.attrs['placeholder'] = 'Address 1'
        self.fields['address2'].widget.attrs['placeholder'] = 'Address 2'
        self.fields['city'].widget.attrs['placeholder'] = 'City'
        self.fields['zipcode'].widget.attrs['placeholder'] = 'Zip Code'


class DeleteAddressForm(forms.Form):
    pass


class CreditCardForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreditCardForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['placeholder'] = 'My Discover'
        self.fields['number'] = forms.CharField(widget=forms.TextInput(
            attrs={'id': 'creditcard-number'}))
        self.fields['number'].widget.attrs[
            'placeholder'] = '123456789'
        self.fields['expdate_month'] = ChoiceField(choices=MONTHS)
        self.fields['expdate_year'] = ChoiceField(choices=YEARS)
        self.fields['securitycode'].widget.attrs[
            'placeholder'] = '123'

    class Meta:
        model = CreditCard
        fields = [
            'name', 'number', 'expdate_month', 'expdate_year', 'securitycode'
        ]

    def clean(self):
        # errors
        self.error_messages = []

        # Card number block
        number = self.cleaned_data['number']

        visa_pattern = r'^4[0-9]{12}(?:[0-9]{3})?$'
        mastercard_pattern = r'^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$'
        americanexpress_pattern = r'^3[47][0-9]{13}$'
        discover_pattern = r'^6(?:011|5[0-9]{2})[0-9]{12}$'

        patterns_list = [
            discover_pattern,
            visa_pattern,
            mastercard_pattern,
        ]
        pattern_string = '|'.join(patterns_list)

        pattern1 = re.compile(pattern_string)  # 3 digits of security code
        pattern2 = re.compile(
            americanexpress_pattern)  # four digits security code

        if pattern1.match(str(number)):
            security_code_pattern = re.compile(r'^[0-9]{3}$')  # 3
        elif pattern2.match(str(number)):
            security_code_pattern = re.compile(r'^[0-9]{4}$')  # 4
        else:
            security_code_pattern = None

        if not pattern1.match(str(number)) and not pattern2.match(str(number)):
            self.error_messages.append('Credit card number not valid')
            # self._errors['number'] = 'Please enter a valid credit card number'

        # Expiration date block
        month = int(self.cleaned_data['expdate_month'])
        year = int(self.cleaned_data['expdate_year'])
        expdate = datetime.datetime(year, month, 1)  # first day of the month
        today = datetime.datetime.today()

        if expdate < today:
            self.error_messages.append('Card has expired')

        # Security code block
        security_code = self.cleaned_data['securitycode']

        # if not security_code_pattern created or does not match the work the errors
        if not security_code_pattern or not security_code_pattern.match(
                str(security_code)):
            self.error_messages.append('Invalid security code')
            # self._errors[
            #     'securitycode'] = 'Please verify the credit card security code'

        self.error_message = ''
        if len(self.error_messages):
            self.error_message = ' & '.join(self.error_messages)
            raise forms.ValidationError(' & '.join(self.error_messages))

        return self.cleaned_data


class DeleteCreditCardConfirmation(forms.Form):
    pass
