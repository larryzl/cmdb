from django.shortcuts import render,redirect
from users.models import department_Mode,CustomUser
from django import forms
import time


class department_from(forms.ModelForm):
    class Meta:
        model = department_Mode
        fields = "__all__"

class user_edit_form(forms.ModelForm):

    department = forms.ModelChoiceField(
        label="部门",
        queryset=department_Mode.objects.all()

    )
    class Meta:
        model = CustomUser
        fields = ["username","first_name","email","mobile","department","user_key"]

def user_edit(request,uid):
    header_title = [
        "用户管理","修改用户"
    ]
    title = header_title[-1]

    data_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    user_obj = CustomUser.objects.get(uuid=uid)

    if request.method == "POST":
        form = user_edit_form(request.POST,instance=user_obj)
        if form.is_valid():
            form.save()
            return redirect('user_list')
        else:
            print(form)


    form = user_edit_form(instance=user_obj)

    return render(request,'users/user_edit.html',locals())
