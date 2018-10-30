from django.db import models
from django.forms import fields

from django import forms
from users.models import CustomUser,department_Mode




manager_demo = [(i, i) for i in (u"经理", u"主管", u"项目责任人", u"管理员", u"BOOS")]
Department = [(u"ops", u"plat", u'dev')]
auth_id = [(u"普通用户", u"普通用户"), (u"管理员", u"管理员")]
auth_gid = [(1001, u"运维部"), (1002, u"架构"), (1003, u"研发"), (1004, u"测试")]


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(
        required=True,
        label="密码",
        widget=forms.PasswordInput()
    )
    renewpassword = forms.CharField(
        required=True,
        label="确认密码",
        widget=forms.PasswordInput()
    )

    # department = forms.ChoiceField(
    #     label="部门",
    #     choices = department_Mode.objects.values_list('id','department_name')
    # )


    class Meta:
        model = CustomUser
        fields = ('username','password','renewpassword','first_name', 'email', 'department', 'mobile', "user_key")
