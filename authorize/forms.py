from django import forms
from authorize.models import auth_group,user_auth_cmdb

class AuthGroupForms(forms.ModelForm):

    class Meta:
        model = auth_group
        fields = "__all__"

class AuthGroupManagerForms(forms.ModelForm):

    class Meta:
        model = user_auth_cmdb
        fields = "__all__"