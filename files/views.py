from django.shortcuts import render,HttpResponse,redirect
from django import forms
from users.models import CustomUser
from files.models import Files
from files.forms import UploadFileForm,FileListForm
# Create your views here.



def handle_uploaded_file(f,fname):
    with open('upload/%s' % fname, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def file_list(request):
    header_title = [
        "文件管理","文件列表"
    ]
    title = header_title[-1]
    user_obj = CustomUser.objects.get(email=request.user)
    if user_obj.is_superuser:
        files = Files.objects.all()
    else:
        files = Files.objects.all().filter(user__email=request.user)

    return render(request,'files/file_list.html',locals())


def upload_file(request):
    header_title = [
        "文件管理","上传文件"
    ]
    title = header_title[-1]

    if request.method == "POST":
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            print(form)

            description = request.POST.get('description')
            filename = form.cleaned_data['file_name']
            user_obj = CustomUser.objects.get(email=request.user)

            files = Files()
            files.file_name =  filename
            files.description = description
            files.user = user_obj
            files.save()

            handle_uploaded_file(request.FILES['file_name'],filename)
            return redirect('file_list')
        else:
            print(form)
    else:
        form = UploadFileForm()

    return render(request,'files/upload.html',locals())


def download(request):
    pass