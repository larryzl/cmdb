from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from users.models import CustomUser
from ansible_api.api import ansible_run
from assets.models import Server
from django.contrib.auth.decorators import login_required
from files.models import Files,AnsibleScript,AnsiblePlaybook
from accounts.auth_api import get_node_list
# Create your views here.

@csrf_exempt
@login_required()
def getServerList(request):
    '''
    datatable 获取主机列表
    :param request:
    :return:
    '''
    server_all = get_node_list(request)
    print(server_all)

    if request.method == "POST":

        postData = request.POST
        for i in postData:
            if i.startswith('order[0][column]'):
                orderColumnName = "columns[%s][name]" % postData.get(i,1)
                orderColumnValue = postData.get(orderColumnName)
            if i == 'order[0][dir]':
                orderDirValue = postData.get(i)
            if i == 'search[value]':
                searchValue = postData.get(i)

        displayLength = request.POST.get('length',10)
        displayStart = int(request.POST.get('start',0))
        draw = postData.get('draw',1)

        # last_time = Server.objects.order_by('-create_time').first().create_time

        # server_all = Server.objects.filter(create_time=last_time).order_by('create_time')
        try:
            if orderColumnValue:
                if orderDirValue == 'desc':
                    server_all = server_all.order_by('-%s' % orderColumnValue)
                else:
                    server_all = server_all.order_by('%s' % orderColumnValue)
        except:
            pass
        try:
            if searchValue:
                server_all = server_all.filter(Q(name__icontains=searchValue)|Q(idc_name__name__icontains=searchValue)
                                               |Q(project__name__icontains=searchValue))
        except:
            pass

        resultLength = server_all.count()

        paginator = Paginator(server_all,displayLength)

        try:
            server_all = paginator.page(displayStart / 10 + 1)
        except PageNotAnInteger:
            server_all = paginator.page(1)
        except EmptyPage:
            server_all = paginator.page(paginator.num_pages)

        dataTable = {
            'draw': draw,
            'recordsTotal': resultLength,
            'recordsFiltered': resultLength
        }
        data = []
        for item in server_all:
            project = [ x[2] for x in item.project.values_list()]
            lable = [ x[2] for x in item.label.values_list()]
            hardware = [item.cpu_nums,item.mem,item.disk]

            row = {
                'id':str(item.uuid),
                'name':str(item.name),
                'ip':item.ip,
                'project':project,
                'label':lable,
                'is_active':item.is_active,
                'idc':item.idc_name.name,
                'hardware':hardware
            }

            data.append(row)
        dataTable['data'] = data

        return HttpResponse(json.dumps(dataTable, ensure_ascii=False))

@csrf_exempt
@login_required()
def displayServerList(request):
    '''
    selectpicker 任务管理模块获取主机列表
    :param request:
    :return:
    '''
    if request.is_ajax():
        try:
            data = json.loads(request.POST.get('data'))
            # print(data)
            server_select = get_node_list(request)

            
            query = {}
            for i,v in data.items():
                if not v:continue
                if i == 'idc_select':
                    query['idc_name__uuid__in'] = v
                elif i == 'project_select':
                    query['project__uuid__in'] = v
                elif i == 'label_select':
                    query['label__uuid__in'] = v

            server_select = server_select.filter(**query).values('name','uuid')
            res_data = [x for x in server_select]
            # print(res_data)
            res = {'status':'success','data':res_data}
        except:
            res = {'status':'failed','data':''}



        return HttpResponse(json.dumps(res,ensure_ascii=Files))



@login_required()
def server_update(request):
    if request.is_ajax():
        sid = request.GET.get('id')
        module = 'setup'
        user_key = CustomUser.objects.get(email=request.user).user_key
        result = ansible_run(user_key=user_key,server_id=sid,obj=Server.objects.filter(is_active=True),module=module)
        data = result

        update_date = []

        for each in data:
            if each == "success":
                for ip in data[each]:
                    ansible_processor_vcpus = data[each][ip]['ansible_facts']['ansible_processor_vcpus']

                    ansible_memtotal_mb = data[each][ip]['ansible_facts']['ansible_memtotal_mb']
                    device_size = 0
                    device_size_list = []
                    for device_name,device_detail in data[each][ip]['ansible_facts']['ansible_devices'].items():
                        # print(device_name)
                        if device_name.startswith('cciss'):
                            # print(device_detail['size'])
                            device_size_list.append(device_detail['size'])
                        elif device_name.startswith('vd'):
                            device_size_list.append(device_detail['size'])
                        elif device_name.startswith('sd'):
                            device_size_list.append(device_detail['size'])
                    for i in device_size_list:
                        i = i.split()
                        if i[1] == "TB":
                            i[0] = float(i[0])*1000
                        elif i[1] == 'MB':
                            i[0] = float(i[0])/1000
                        else:
                            i[0] = float(i[0])
                        device_size += i[0]

                    update_date.append(
                            {
                                ip:{
                                    'ansible_processor_vcpus':ansible_processor_vcpus,
                                    'ansible_memtotal_mb':str(int(int(ansible_memtotal_mb)/1000)) + "G",
                                    'device_size':str(device_size) + 'GB'
                                }
                            }
                    )
        for item in update_date:
            for ip,values in item.items():
                s_obj = Server.objects.filter(ip=ip)
                s_obj.update(
                    cpu_nums=values['ansible_processor_vcpus'],
                    mem = values['ansible_memtotal_mb'],
                    disk = values['device_size']
                )
        # print(json.dumps(update_date))
        # for k,v in data['success'].items():
        #     print(v)
        return HttpResponse(json.dumps(data,ensure_ascii=False))


def file_detail(request):
    if request.is_ajax():
        file_id = request.GET.get('id')
        file_type = request.GET.get('t')
        print(file_type)
        try:

            if file_type == 's':
                file_data = AnsibleScript.objects.get(uuid=file_id)
            elif file_type == 'f':
                file_data = Files.objects.get(uuid=file_id)
            elif file_type == 'p':
                file_data = AnsiblePlaybook.objects.get(uuid=file_id)
            res = {
                '文件名':str(file_data.file_name).split('/')[-1],
                '文件大小':str(file_data.file_size),
                '创建时间':file_data.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
                '创建用户':str(file_data.user.first_name),
                '描述':str(file_data.description),
                'MD5':str(file_data.md5)
            }
        except:
            res = {"status":"error"}

        # print(res)


        return HttpResponse(json.dumps(res,ensure_ascii=Files))

def ajax_ansible_cmd(request):
    '''
    执行ansible 方法
    :param request:
    :return:
    '''
    email = request.session.get('email')
    user_key = CustomUser.objects.get(email=email).user_key

    if request.is_ajax():
        import os
        # print(request.POST)

        ansible_module = request.POST.get('module')
        server_id = request.POST.get('server_id')
        args = ''

        if ansible_module == 'shell':
            args = request.POST.get('args')
        elif ansible_module == 'copy':
            file_id = request.POST.get('file_id')
            file_path = request.POST.get('args')
            try:
                fileObj = Files.objects.get(uuid=file_id)
            except:
                return HttpResponse(json.dumps({'status':'error'}))
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            args = "src=%s/%s dest=%s" % (BASE_DIR,fileObj.file_name,file_path)
        elif ansible_module == 'script':
            file_id = request.POST.get('file_id')
            file_path = request.POST.get('args')
            script_args = request.POST.get('script_args','')
            # print(file_id)
            # print(file_path)
            try:
                fileObj = AnsibleScript.objects.get(uuid=file_id)
            except:
                return HttpResponse(json.dumps({'status':'error'}))
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            args = "chdir=%s %s/%s %s" % (file_path,BASE_DIR,fileObj.file_name,script_args)
        elif ansible_module == 'playbook':
            file_id = request.POST.get('file_id')
            args = request.POST.get('args')
            try:
                fileObj = AnsiblePlaybook.objects.get(uuid=file_id)
            except:
                return HttpResponse(json.dumps({'status':'error'}))


        else:
            pass

        result = {}
        print('module:',ansible_module)
        print("args:" ,args)
        if ansible_module == 'playbook':
            playbook_list = []
            playbook_list.append(str(fileObj.file_name))
            ansible_run(user_key=user_key,server_id=server_id,obj=Server.objects.filter(is_active=True),module=ansible_module,args=args,playbook=playbook_list)
            result = {"status":'sucess'}
        else:
            result = ansible_run(user_key=user_key,server_id=server_id,obj=Server.objects.filter(is_active=True),module=ansible_module,args=args)
        # result = ansible_run.get_result()
        # print(result)
        # print(result)
        return HttpResponse(json.dumps(result))

def reViewPlaybook(request):
    if request.is_ajax():
        import os
        uid = request.GET.get('uid')
        file_path = str(AnsiblePlaybook.objects.get(uuid = uid).file_name)
        print(type(file_path))
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(type(BASE_DIR))
        with open(os.path.join(BASE_DIR,file_path)) as f:
            file_data = f.readlines()

        result = {'data':file_data}

        return HttpResponse(json.dumps(result))