from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.contrib.auth.models import User
from users.models import CustomUser
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.hashers import make_password,check_password
from .forms import RegistrationFrom,LoginForm,DepartmentForm,NewPasswordForm
#,ProfileForm,PwdchangeForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from accounts.models import UserCreateForm
from users.models import cmdb_uuid,department_Mode,auth_gid
from cmdb.settings import EMAIL_PUSH
import hashlib
from django.core.mail import send_mail
from django.template import RequestContext
import time
from django.views.decorators.csrf import csrf_protect
from accounts.auth_api import has_auth

auth_key = ""

# Create your views here.
def register(request):
    header_title = [
        "用户管理","添加用户"
    ]
    title = header_title[-1]
    content = {}
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.is_staff = 1
            password = form.cleaned_data['password']
            new_user = form.save(commit=False)

            new_user.is_staff = 1
            new_user.session_key = ""
            new_user.uuid = cmdb_uuid()

            new_user.password = make_password(password, None, 'pbkdf2_sha256')
            new_user.save()

            # if EMAIL_PUSH:
            #     token = str(hashlib.sha1(new_user.username + auth_key + new_user.uuid +
            #                              time.strftime('%Y-%m-%d', time.localtime(time.time()))).hexdigest())
            #     #
            #     url = u'http://%s/accounts/newpasswd/?uuid=%s&token=%s' % (request.get_host(), new_user.uuid, token)
            #     mail_title = u'运维自动化初始密码,注意密码设置需符合8位以上,字母+数字+特殊符合组合的形式'
            #     mail_msg = u"""
            #     Hi,%s:
            #         请点击以下链接初始化运维自动化密码,此链接当天有效
            #         注意密码设置需符合8位以上，字母+数字+特殊符合组合的形式，否则无法登录::
            #             %s
            #         有任何问题，请随时和运维组联系。
            #     """ % (new_user.first_name, url)
            #     #
            #
            #     send_mail(mail_title, mail_msg, u'运维自动化<devops@funshion.net>', [new_user.email], fail_silently=False)


            return HttpResponseRedirect('/users/user/list')
        else:
            data = UserCreateForm()
            print(form)
            return render(request,'users/reg.html', locals())
    else:
        data = UserCreateForm()
        print('b')
        return render(request,'users/reg.html', locals())

def Logout(request):
    request.session.flush()
    return HttpResponseRedirect("/users/login/")

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(username,password)
            try:
                data = CustomUser.objects.get(username=username)
                check_data = check_password(password,data.password)
                if check_data:
                    data.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request,data)
                    # auth_data = auth_class(request.user)

                    return HttpResponseRedirect('/')
                else:
                    message = "密码错误"
                    # 登陆失败
                    print(message)
                    return render(request, 'users/login.html', locals())
            except:
                message = "用户名不存在"
                print(form)
                # print(message)
                return render(request,'users/login.html',locals())
        else:
            print(form)
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})

# @has_auth
@login_required()
def user_list(request):
    header_title = [
        "用户管理","用户列表"
    ]
    title = header_title[-1]

    users = CustomUser.objects.all().filter(is_staff=True)
    return render(request,'users/user_list.html',locals())

def user_del(request,sid):

    user = CustomUser.objects.get(pk=sid)
    user.is_staff = False
    user.is_active = False
    user.save()
    return HttpResponse('ok')


def department_list(request):
    header_title = [
        "部门管理","部门列表"
    ]
    title = header_title[-1]

    departments = department_Mode.objects.all()
    content = {}
    for d in departments:
        dep_user_list = []
        dep_user_all = d.users.all().values("first_name")

        for t in dep_user_all:
            dep_user_list.append(t.get("first_name"))
        for dg in auth_gid:
            if d.desc_gid == dg[0]:
                dep_group_name = dg[1]
                break
        else:
            dep_group_name = "部门组错误"
        # print(d.description)
        content[d.department_name] = {"department_id":d.id,
                                      'user_list':dep_user_list,
                                      'department_admin':d.department_admin,
                                      'department_group':dep_group_name,
                                      'department_desc':d.description
                                      }


    return render(request,'users/department_list.html',locals())

def department_add(request):
    header_title = [
        "部门管理","添加部门"
    ]
    title = header_title[-1]

    if request.method == 'POST':
        form = DepartmentForm(request.POST)

        if form.is_valid():
            form.save()
        return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request,'users/department_add.html',locals())


def department_edit(request,id):
    header_title = [
        "部门管理","修改部门"
    ]
    title = header_title[-1]
    data = department_Mode.objects.get(id=id)
    if request.method == 'POST':
        uf = DepartmentForm(request.POST, instance=data)
        u"验证数据有效性"
        if uf.is_valid():
            uf.save()
        return redirect('department_list')

    uf = DepartmentForm(instance=data)
    return render(request,'users/department_edit.html', locals())


def department_del(request,sid):

    department_Mode.objects.get(id=sid).delete()
    return HttpResponse('ok')