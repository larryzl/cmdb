from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required

from assets.models import Server,IDC

@login_required
def index(requests):
    title = "主页"
    context = {"title":title}
    return render(requests,'index.html',context=context)


def test_html(request):
    server_all = Server.objects.all()

    idcs = IDC.objects.all()
    return render(request,'test.html',locals())


def error_auth(request):

    return render(request,'error_auth.html',locals())

def page_not_found(request):
    return render(request,'404.html')