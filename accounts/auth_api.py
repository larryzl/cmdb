from authorize.models import auth_group,user_auth_cmdb
from django.shortcuts import redirect

def has_auth(func):
    def auth(request,*args,**kwargs):
        if not request.session.get('username'):
            return redirect('login')
        return func(request,*args,**kwargs)
    return auth

