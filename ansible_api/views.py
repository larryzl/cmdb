from django.shortcuts import render
from .api import AnsibleRunner,AnsibleHost,ansible_run
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from assets.models import Server,IDC,Project,Label
from django.http import HttpResponse,JsonResponse
import json
import tempfile
import os
from django.db.models import Q
import stat
from users.models import CustomUser
from files.models import Files,AnsibleScript,AnsiblePlaybook
from accounts.auth_api import has_auth,get_node_list

# Create your views here.


@has_auth('exec_cmd')
@login_required
@csrf_exempt
def exec_cmd(request):
    header_title = [
        "任务管理","主机操作"
    ]
    title = header_title[-1]

    idcs = IDC.objects.filter()
    projects = Project.objects.filter()
    labels = Label.objects.filter()

    email = request.session.get('email')
    userObj = CustomUser.objects.get(email=email)

    if userObj.is_superuser:
        files = Files.objects.all()
        user_scripts = AnsibleScript.objects.all()
        user_playbook = AnsiblePlaybook.objects.all()
    else:
        files = Files.objects.filter(Q(user__email=email)|Q(is_shared=True))
        user_scripts = AnsibleScript.objects.filter(Q(user__email=email)|Q(is_shared=True))
        user_playbook = AnsiblePlaybook.objects.filter(Q(user__email=email)|Q(is_shared=True))

    file_data = []
    scripts_data = []
    playbook_data = []
    for i in user_scripts:
        scripts_data.append(
                {
                    'file_name':str(i.file_name).split('/')[-1],
                    'create_time':i.date_joined,
                    'file_size':i.file_size,
                    'description':i.description,
                    'file_id':i.uuid,
                    'md5':i.md5
                }
        )

    for i in files:
        file_data.append(
                {
                    'file_name':str(i.file_name).split('/')[-1],
                    'create_time':i.date_joined,
                    'file_size':i.file_size,
                    'description':i.description,
                    'file_id':i.uuid,
                    'md5':i.md5
                }
        )
    for i in user_playbook:
        playbook_data.append(
                {
                    'file_name':str(i.file_name).split('/')[-1],
                    'create_time':i.date_joined,
                    'file_size':i.file_size,
                    'description':i.description,
                    'file_id':i.uuid,
                    'md5':i.md5
                }
        )
    return render(request,'ansible/ansible_cmd.html',locals())

def playbookView(request):
    import os
    uid = request.GET.get('uid')
    file_path = str(AnsiblePlaybook.objects.get(uuid = uid).file_name)
    file_name = file_path.split('/')[-1]
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(BASE_DIR,file_path)) as f:
        file_data = f.readlines()


    return render(request,'ansible/playbook_view.html',locals())


def ansible_log(request):
    pass
