from django.shortcuts import render,HttpResponse,redirect
from django import forms
from django.contrib.auth.decorators import login_required
from accounts.auth_api import has_auth
from users.models import CustomUser
from django.db.models import Q
from files.models import Files,AnsibleScript,AnsiblePlaybook
import hashlib
import os
from files.forms import UploadFileForm,FileListForm,UploadScriptForm,UploadPlaybookForm
from api.api import bytes2human
# Create your views here.

def getFileMd5(filename):
        if not os.path.isfile(filename):
                return
        mhash = hashlib.md5()
        f = open(filename,'rb')
        while True:
                b = f.read(8096)
                if not b:
                        break
                mhash.update(b)
        f.close()
        return mhash.hexdigest()

def handle_uploaded_file(f,fname):
    with open('upload/files/%s' % fname, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    size = bytes2human(os.path.getsize('upload/files/%s'%fname))
    md5 = getFileMd5('upload/files/%s'%fname)
    return (size,md5)


@has_auth('file_list')
@login_required
def file_list(request):
    header_title = [
        "文件管理","文件列表"
    ]
    email = request.session.get('email')
    title = header_title[-1]
    user_obj = CustomUser.objects.get(email=email)
    if user_obj.is_superuser:
        files = Files.objects.all()
    else:
        files = Files.objects.filter(Q(user__email=email)|Q(is_shared=True))

    return render(request,'files/file_list.html',locals())

@has_auth('upload_file')
@login_required
def upload_file(request):
    header_title = [
        "文件管理","上传文件"
    ]
    title = header_title[-1]

    if request.method == "POST":
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            is_shared =  request.POST.get('is_shared')

            description = request.POST.get('description')
            filename = form.cleaned_data['file_name']
            email = request.session.get('email')
            user_obj = CustomUser.objects.get(email=email)


            files = Files()
            files.file_name =  filename
            files.description = description
            files.user = user_obj
            size,md5 = handle_uploaded_file(request.FILES['file_name'],filename)

            files.md5 = md5
            files.file_size = size
            # if
            # files.is_shared
            if is_shared:files.is_shared = True

            files.save()

            return redirect('file_list')
    else:
        form = UploadFileForm()
    return render(request,'files/upload.html',locals())

def scripts_list(request):
    header_title = [
        "文件管理","脚本列表"
    ]
    title = header_title[-1]

    email = request.session.get('email')
    user_obj = CustomUser.objects.get(email=email)
    if user_obj.is_superuser:
        files = AnsibleScript.objects.all()
    else:
        files = AnsibleScript.objects.filter(Q(user__email=request.user)|Q(is_shared=True))

    return render(request,'files/scripts.html',locals())

def upload_script(request):
    header_title = [
        "文件管理","编辑脚本"
    ]
    title = header_title[-1]

    if request.method == "POST":
        form = UploadScriptForm(request.POST,request.FILES)
        if form.is_valid():
            is_shared =  request.POST.get('is_shared')

            description = request.POST.get('description')
            filename = form.cleaned_data['file_name']
            email = request.session.get('email')
            user_obj = CustomUser.objects.get(email=email)


            files = AnsibleScript()
            files.file_name =  filename
            files.description = description
            files.user = user_obj
            size,md5 = handle_uploaded_file(request.FILES['file_name'],filename)

            files.md5 = md5
            files.file_size = size
            # if
            # files.is_shared
            if is_shared:files.is_shared = True

            files.save()

            return redirect('scripts')
    else:
        form = UploadFileForm()
    return render(request,'files/scripts_upload.html',locals())

def scripts_list(request):
    header_title = [
        "文件管理","脚本列表"
    ]
    title = header_title[-1]

    email = request.session.get('email')
    user_obj = CustomUser.objects.get(email=email)
    if user_obj.is_superuser:
        files = AnsibleScript.objects.all()
    else:
        files = AnsibleScript.objects.filter(Q(user__email=request.user)|Q(is_shared=True))

    return render(request,'files/scripts.html',locals())

def playbook_list(request):
    header_title = [
        "文件管理","Playbook列表"
    ]
    title = header_title[-1]

    email = request.session.get('email')
    user_obj = CustomUser.objects.get(email=email)
    if user_obj.is_superuser:
        files = AnsiblePlaybook.objects.all()
    else:
        files = AnsiblePlaybook.objects.filter(Q(user__email=request.user)|Q(is_shared=True))

    return render(request,'files/playbook.html',locals())

def upload_playbook(request):
    header_title = [
        "文件管理","上传Playbook"
    ]
    title = header_title[-1]

    if request.method == "POST":
        form = UploadPlaybookForm(request.POST,request.FILES)
        if form.is_valid():
            is_shared =  request.POST.get('is_shared')
            description = request.POST.get('description')
            filename = form.cleaned_data['file_name']
            email = request.session.get('email')
            user_obj = CustomUser.objects.get(email=email)

            files = AnsiblePlaybook()
            files.file_name =  filename
            files.description = description
            files.user = user_obj
            size,md5 = handle_uploaded_file(request.FILES['file_name'],filename)

            files.md5 = md5
            files.file_size = size
            # if
            # files.is_shared
            if is_shared:files.is_shared = True

            files.save()

            return redirect('playbook')
    else:
        form = UploadFileForm()
    return render(request,'files/playbook_upload.html',locals())


def download(request):
    pass