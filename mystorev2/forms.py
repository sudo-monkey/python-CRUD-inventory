from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import fields, models
from mystorev2.models import User

from django.forms.models import fields_for_model
from .models import User, Warehouse, Product
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Field, Fieldset, MultiField, Layout, LayoutObject

# Render form for new warehouse


class WarehouseForm(forms.ModelForm):
    # used to set css classes to the various fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['wh_name'].widget.attrs.update(
            {'class': 'textinput form-control'})
        self.fields['wh_desc'].widget.attrs.update(
            {'class': 'textinput form-control', 'min': '0'})

    class Meta:
        model = Warehouse
        fields = ('wh_name', 'wh_desc')

# Render form for new product


class ProductForm(forms.ModelForm):
    # used to set css classes to the various fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prod_name'].widget.attrs.update(
            {'class': 'textinput form-control', 'min': '0'})
        self.fields['prod_desc'].widget.attrs.update(
            {'class': 'textinput form-control'})
        self.fields['prod_qty'].widget.attrs.update(
            {'class': 'textinput form-control', 'min': '0'})
        self.fields['prod_prodkey'].widget.attrs.update(
            {'class': 'textinput form-control', 'min': '0'})

    class Meta:
        model = Product
        fields = ['prodkey', 'prod_name', 'prod_desc', 'prod_qty']


########### USER MANAGEMENT FORMS ############

# Render form for new user registration
class RegistrationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'password',
                  'group', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('btn_register', 'Register'))

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# Render form for user access control (ACL)


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username',
                  'is_staff',
                  'group'
                  ]
        labels = {
            'username': 'Username',
            'is_staff': 'Staff',
            'group': 'Department',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.helper = FormHelper()
        # self.helper.form_method = 'post'
        # self.helper.add_input(Submit('btn_register', 'Register'))

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set.staff("True")
        if commit:
            user.save()
        return user

# Render form for group access control (RBAC)


class GroupUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username',
                  'is_staff',
                  'group'
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.helper = FormHelper()
        # self.helper.form_method = 'post'
        # self.helper.add_input(Submit('btn_register', 'Register'))

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set.staff("True")
        if commit:
            user.save()
        return user
