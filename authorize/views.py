from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from authorize.models import auth_group,user_auth_cmdb
from authorize.forms import AuthGroupForms,AuthGroupManagerForms

# Create your views here.
@login_required
def auth_index(request):
    """
    权限首页
    :param request:
    :return:
    """
    header_title = [
        "访问管理","权限组列表"
    ]
    title = header_title[-1]
    data = auth_group.objects.all().order_by("-date_time")
    group_user_count = {}

    for i in data:
        # data_id = auth_group.objects.get(uuid=i.uuid)
        group_user_count[i.uuid] = i.group_user.all().count()

    return render(request,'auth/index.html', locals())

def auth_add(request):
    header_title = [
        "访问管理","添加权限组"
    ]
    title = header_title[-1]
    if request.method == "POST":
        form = AuthGroupForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('auth_list')
    else:
        form  = AuthGroupForms()

    return render(request,'auth/auth_add.html',locals())


def auth_edit(request,id):
    header_title = [
        "访问管理","编辑权限组"
    ]

    title = header_title[-1]
    form = AuthGroupForms(instance=auth_group.objects.get(uuid=id))
    if request.method == "POST":
        form = AuthGroupForms(request.POST,instance=auth_group.objects.get(uuid=id))
        if form.is_valid():
            form.save()
            return redirect('auth_list')

    return render(request,'auth/auth_edit.html',context=locals())

def auth_del(request):
    pass

def auth_group_authorize(request,id):
    '''
    访问授权页面
    :param request:
    :return:
    '''
    header_title = [
        "访问管理","权限管理"
    ]
    authGroupObj = auth_group.objects.get(uuid=id)
    try:
        uaObj = user_auth_cmdb.objects.get(group_name__uuid=id)
        data = AuthGroupManagerForms(instance=uaObj)
    except:
        data = AuthGroupManagerForms()

    if request.method == "POST":
        try:
            form = AuthGroupManagerForms(request.POST,instance=uaObj)
        except:
            form = AuthGroupManagerForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('auth_list')
    return render(request,'auth/auth_manager.html',locals())







