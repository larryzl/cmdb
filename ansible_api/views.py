from django.shortcuts import render
from .api import AnsibleRunner,AnsibleHost,ansible_run
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from assets.models import Server,IDC,Project,Label
from django.http import HttpResponse,JsonResponse
import json
import tempfile
import os
import stat
from users.models import CustomUser

# Create your views here.

def index(request):
    header_title = [
        "任务管理","主机操作"
    ]
    title = header_title[-1]

    data = Server.objects.filter(is_active=True)

    return render(request,'ansible/index.html',locals())

@login_required
@csrf_exempt
def exec_cmd(request):
    header_title = [
        "任务管理","批量命令"
    ]
    title = header_title[-1]

    server_all = Server.objects.filter(is_active=True)
    idcs = IDC.objects.filter()
    projects = Project.objects.filter()
    labels = Label.objects.filter()

    user_key = CustomUser.objects.get(email=request.user).user_key


    if request.is_ajax():
        module = request.POST.get('comm_shell')
        cmd = request.POST.get('ansible_cmd')
        server_id = request.POST.get('server_id')

        host_list = []
        host_dict = []

        ssh_keyfile = tempfile.mktemp()
        # print(ssh_keyfile)
        with open(ssh_keyfile, 'w+', encoding='utf-8') as file:
            file.write(user_key)
        os.chmod(ssh_keyfile,stat.S_IRUSR|stat.S_IWUSR)
        for id in server_id.split(','):
            server_obj = server_all.get(id=id)
            host_dict.append(
                    {
                        'host': server_obj.ip,
                        'port': server_obj.ssh_port,
                        'method':'ssh',
                        'user': server_obj.ssh_user,
                        'ssh_key':ssh_keyfile
                    }
            )
        # print(host_dict)

        for i in host_dict:
            host_list.append(AnsibleHost(host=i['host'],port=i['port'],connection=i['method'],ssh_user=i['user'],ssh_key=i['ssh_key']))

        task = AnsibleRunner(host_list)

        task.run(module,cmd)
        result = task.get_result()
        # result = ansible_run.get_result()
        # print(result)
        os.remove(ssh_keyfile)
        # print(result)
        return HttpResponse(json.dumps(result))


    return render(request,'ansible/ansible_cmd.html',locals())


