from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from users.models import CustomUser
from ansible_api.api import ansible_run
from assets.models import Server
from django.contrib.auth.decorators import login_required
# Create your views here.

@csrf_exempt
@login_required()
def getServerList(request):

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
        server_all = Server.objects.all()
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