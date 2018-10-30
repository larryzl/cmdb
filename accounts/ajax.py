from django.shortcuts import render,HttpResponse,redirect
from users.models import department_Mode

def verifyForm(request):
    type = request.POST.get('type')
    print(type)

