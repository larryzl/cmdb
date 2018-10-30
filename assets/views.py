from django.shortcuts import render,HttpResponse,redirect
from django.db.models import Q
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from assets.forms import ServerEditFrom,ServerFrom,IdcForm,ProjectFrom,LabelForm
from assets.models import Server,IDC,Project,Label,server_os
# Create your views here.

def index(request):
    return HttpResponse("ok")

@login_required()
def server_list(request):

    header_title = [
        "主机管理","主机列表"
    ]
    title = header_title[-1]

    return render(request,'assets/server_list.html',context=locals())

@login_required()
def server_edit(request,id):
    header_title = [
        "主机管理","编辑主机"
    ]
    title = header_title[-1]
    form = ServerEditFrom(instance=Server.objects.get(uuid=id))
    if request.method == "POST":
        form = ServerFrom(request.POST,instance=Server.objects.get(uuid=id))
        if form.is_valid():
            form.save()
            return redirect('server_list')

    return render(request,'assets/server_edit.html',context=locals())

@login_required()
def server_add(request):
    header_title = [
        "主机管理","添加主机"
    ]
    title = header_title[-1]
    form = ServerFrom()
    if request.method == "POST":
        form = ServerFrom(request.POST)
        if form.is_valid():
            form.save()
            return redirect('server_list')
        else:
            print(form)
    return render(request,'assets/server_add.html',context=locals())

@login_required()
def server_add_batch(request):
    header_title = [
        "主机管理","批量添加添加主机"
    ]
    title = header_title[-1]

    idcs = IDC.objects.all()
    os_list = server_os
    if request.method == 'POST':
        idc = request.POST.get('idc')
        name_tag = request.POST.get('name')
        ip_list = request.POST.getlist('ip')
        os = request.POST.get('os')
        for ip in ip_list:
            name = name_tag+ip.split('.')[-1]
            idc_name = IDC.objects.get(pk=idc)
            # try:
            Server.objects.create(name=name,ip=ip,idc_name=idc_name,system=os,ssh_port=22,ssh_user='root')
            # except:
            #     print(name,idc_name)
        return redirect('server_list')

    return render(request, 'assets/server_add_batch.html',locals())

@login_required()
def server_del(request):
    '''
    删除主机
    :param request:
    :param sid:
    :return:
    '''
    if request.method == "DELETE":
        sid = request.GET.get('id')
        print(sid)
        if "," in sid:
            server_obj = Server.objects.filter(uuid__in=sid.split(','))
        else:
            server_obj = Server.objects.filter(uuid=sid)

        try:
            server_obj.delete()
            res = {"status":"ok"}
        except:
            res = {"status":"error"}

        return HttpResponse(json.dumps(res,ensure_ascii=False))


@login_required()
def server_change_status(request):

    if request.is_ajax():
        sid = request.GET.get('id')
        if "," in sid:
            server_obj = Server.objects.filter(uuid__in=sid.split(','))
        else:
            server_obj = Server.objects.filter(uuid=sid)
        for obj in server_obj:
            if obj.is_active:
                obj.is_active = False
            else:
                obj.is_active = True
            obj.save()

        # try:
        #     server_obj.update(is_active=False)
        res = {"status":"ok"}
        # except:
        #     res = {"status":"error"}

        return HttpResponse(json.dumps(res,ensure_ascii=False))


@login_required()
def idc_list(request):

    header_title = [
        "机房管理","机房列表"
    ]
    title = header_title[-1]

    idcs = IDC.objects.all().order_by("name")


    return render(request,'assets/idc_list.html',locals())

@login_required()
def idc_add(request):
    header_title = [
        "机房管理","添加机房"
    ]
    title = header_title[-1]
    form = IdcForm()
    if request.method == "POST":
        form  = IdcForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('idc_list')
        else:
            print(form)

    return render(request,'assets/idc_add.html',locals())

@login_required()
def idc_del(request):
    if request.method == "DELETE":
        sid = request.GET.get('id')
        print(sid)
        if "," in sid:
            idc_obj = IDC.objects.filter(uuid__in=sid.split(','))
        else:
            idc_obj = IDC.objects.filter(uuid=sid)

        try:
            idc_obj.delete()
            res = {"status":"ok"}
        except:
            res = {"status":"error"}

        return HttpResponse(json.dumps(res,ensure_ascii=False))

    print('uuid IN (' + id + ')' )
    IDC.objects.extra(where=[ 'uuid IN (\'' + id + '\')' ]).delete()
    return HttpResponse('ok')
    # return render(request,'assets/server_list.html',locals())

@login_required()
def idc_edit(request,id):
    header_title = [
        "机房管理","修改机房"
    ]
    title = header_title[-1]

    form = IdcForm(instance=IDC.objects.get(uuid=id))
    host_all = Server.objects.all()
    host_select = Server.objects.filter(idc_name=IDC.objects.get(uuid=id))
    host_no_select = [a for a in host_all if a not in host_select]
    if request.method == "POST":
        form = IdcForm(request.POST,instance=IDC.objects.get(uuid=id))
        if form.is_valid():
            if len(request.POST.getlist('host_select')) > 0:
                Server.objects.filter(pk__in=request.POST.getlist('host_select')).update(idc_name=IDC.objects.get(pk=id))
            else:
                print(1)
                IDC.objects.get(uuid=id).server_set.none()
            form.save()
            return redirect('idc_list')
        else:
            print(form)

    return render(request,'assets/idc_edit.html',locals())


@login_required()
def project_list(request):

    header_title = [
        "业务组管理","业务组列表"
    ]
    title = header_title[-1]

    projects = Project.objects.all()

    return render(request, 'assets/project_list.html', context=locals())

@login_required()
def project_add(request):

    header_title = [
        "主机组管理","添加主机组"
    ]
    title = header_title[-1]

    form = ProjectFrom()
    if request.method == "POST":
        form  = ProjectFrom(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
        else:
            print(form)

    return render(request, 'assets/project_add.html', context=locals())

@login_required()
def project_edit(request,id):
    header_title = [
        "主机组管理","修改主机组"
    ]
    title = header_title[-1]
    form = ProjectFrom(instance=Project.objects.get(uuid=id))
    project = Project.objects.get(uuid=id)

    host_all = Server.objects.all()

    host_select = Server.objects.filter(project=project)
    host_no_select = [a for a in host_all if a not in host_select]

    if request.method == "POST":
        form = ProjectFrom(request.POST,instance=Project.objects.get(uuid=id))

        if form.is_valid():
            project.server_set.clear()
            s_host = request.POST.getlist('host_select')
            for h in s_host:
                host = Server.objects.get(pk=h)
                project.server_set.add(host)
            form.save()
            return redirect('project_list')
        else:
            print(form)


    return render(request, 'assets/project_edit.html', context=locals())

@login_required()
def label_list(request):

    header_title = [
        "标签管理","标签列表"
    ]
    title = header_title[-1]
    labels = Label.objects.all()

    return render(request, 'assets/label_list.html', context=locals())

@login_required()
def lable_add(request):
    header_title = [
        "标签管理","添加标签"
    ]
    title = header_title[-1]

    form = LabelForm()
    if request.method == "POST":
        form  = LabelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tag_list')
        else:
            print(form)

    return render(request,'assets/lable_add.html',context=locals())

@login_required()
def lable_edit(request,id):
    header_title = [
        "标签管理","修改标签"
    ]
    title = header_title[-1]

    label = Label.objects.get(uuid=id)

    form = LabelForm(instance=label)

    host_all = Server.objects.all()
    host_select = Server.objects.filter(label=label)
    host_no_select = [a for a in host_all if a not in host_select]

    if request.method == "POST":
        form = LabelForm(request.POST,instance=label.objects.get(uuid=id))
        if form.is_valid():
            label.server_set.clear()
            s_host = request.POST.getlist('host_select')
            for h in s_host:
                host = Server.objects.get(pk=h)
                print(host)
                label.server_set.add(host)

            form.save()
            return redirect('lable_list')


    return render(request,'assets/lable_edit.html',locals())

