from django import forms
from django.contrib.auth import authenticate,login
from users.models import department_Mode,CustomUser

class LoginForm(forms.Form):
    email = forms.CharField(
        required=True,
        label=u"用户名",
        error_messages={'required': '请输入邮箱'},
        widget=forms.TextInput(
            attrs={
                'placeholder':"邮箱",
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label=u"密码",
        error_messages={'required': '请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':"密码",
            }
        ),
    )
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError("邮箱和密码为必填项")
        else:
            cleaned_data = super(LoginForm, self).clean()

class RegistrationFrom(forms.Form):
    username = forms.CharField(required=True,max_length=12,min_length=4)
    password = forms.CharField(required=True,max_length=12,min_length=4)


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = department_Mode
        fields = "__all__"

class NewPasswordForm(forms.ModelForm):
    newpassword = forms.CharField(required=True, max_length=128, min_length=6, label=u'新密码')
    renewpassword = forms.CharField(required=True, max_length=128, min_length=6, label=u'确认密码')

    class Meta:
        model = CustomUser
        fields = ['newpassword', 'renewpassword']
