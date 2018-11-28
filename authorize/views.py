from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from authorize.models import auth_group,user_auth_cmdb,AuthNode,AuthGroupNode
from authorize.forms import AuthGroupForms,AuthGroupManagerForms
from users.models import CustomUser,cmdb_uuid,department_Mode,auth_gid
from django.db.models import Q
from assets.models import Server

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




def arule_index(request):
    '''
    资产授权 主页
    :param request:
    :return:
    '''
    header_title = [
        "主机权限管理","编辑主机权限"
    ]
    title = header_title[-1]

    return render(request,'auth/arule_index.html',locals())

def arule_user_grant_list(request):
    '''
    用户资产授权 列表
    :param request:
    :return:
    '''
    header_title = [
        "主机权限管理","用户授权"
    ]
    title = header_title[-1]

    users = CustomUser.objects.filter(is_active=True).filter(is_staff=True).filter(is_superuser=False)

    return render(request,'auth/arule_user_list.html',locals())

def arule_user_grant(request,uid):
    '''
    编辑用户授权
    :param request:
    :return:
    '''
    header_title = [
        "主机权限管理","用户授权"
    ]
    title = header_title[-1]
    userObj = CustomUser.objects.get(uuid=uid)

    try:
        auth_node = AuthNode.objects.filter(user_name=uid)
        host_select = Server.objects.filter(uuid__in=[n['node_id'] for n in auth_node.values()])
        host_no_select = Server.objects.filter(~Q(uuid__in=[n['node_id'] for n in auth_node.values()]))

    except:
        host_no_select = Server.objects.filter(is_active=True)
        host_select = []

    if request.method == "POST":
        serverSelect = request.POST.getlist('hostSelect')
        serverNoSelect = request.POST.getlist('hostNoSelect')
        for h in serverSelect:
            try:
                AuthNode.objects.get(user_name=userObj.uuid,node=h)
            except:
                AuthNode.objects.create(user_name=userObj,node=Server.objects.get(uuid=h))
        for h in serverNoSelect:
            try:
                AuthNode.objects.get(user_name=userObj.uuid,node=h).delete()
            except:
                continue

        return redirect('arule_user_grant_list')
    return render(request,'auth/arule_user_edit.html',locals())

def arule_depart_grant_list(request):
    '''
    部门授权列表
    :param request:
    :return:
    '''
    header_title = [
        "主机权限管理","部门授权列表"
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

        content[d.department_name] = {"department_id":d.uuid,
                                      'user_list':dep_user_list,
                                      'department_admin':d.department_admin,
                                      # 'department_admin_uuid':d.department_admin.uuid,
                                      'department_group':dep_group_name,
                                      'department_desc':d.description
                                      }
    return render(request,'auth/arule_depart_list.html',locals())

def arule_depart_grant_edit(request,uid):
    header_title = [
        "主机权限管理","部门授权"
    ]
    title = header_title[-1]

    depObj = department_Mode.objects.get(uuid=uid)

    auth_node=AuthGroupNode.objects.filter(department_name = depObj.uuid)
    host_select = Server.objects.filter(uuid__in=[n['node_id'] for n in auth_node.values()])
    host_no_select = Server.objects.filter(~Q(uuid__in=[n['node_id'] for n in auth_node.values()]))

    if request.method == "POST":
        serverSelect = request.POST.getlist('hostSelect')
        serverNoSelect = request.POST.getlist('hostNoSelect')
        for h in serverSelect:
            try:
                AuthGroupNode.objects.get(department_name=depObj.uuid,node=h)
            except:
                AuthGroupNode.objects.create(department_name=depObj,node=Server.objects.get(uuid=h))
        for h in serverNoSelect:
            try:
                AuthGroupNode.objects.get(department_name=depObj.uuid,node=h).delete()
            except:
                continue

        return redirect('arule_depart_grant_list')



    return render(request,'auth/arule_depart_edit.html',locals())
