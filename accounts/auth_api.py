from authorize.models import auth_group,user_auth_cmdb,AuthNode
from assets.models import Server
from django.db.models import Q
from django.shortcuts import redirect
from users.models import CustomUser



def has_auth(view_name):

    def decorator(func):
        def auth(request,*args,**kwargs):
            # print(request.session.items())
            if not request.session.get('email'):
                return redirect('login')
            email = request.session.get('email')
            # print(email)
            userObj = CustomUser.objects.get(email=email)
            # 如果是超级管理员不检查
            if userObj.is_superuser:
                return func(request,*args,**kwargs)
            auth_groups = userObj.user_auth_group.all()
            auth_group_uuid_list = []
            for auth_group in auth_groups:
                if auth_group.enable:
                    auth_group_uuid_list.append(auth_group.uuid)
            # 如果未分配权限组,返回错误页面
            if len(auth_group_uuid_list) == 0:
                return redirect("error_auth")
            uacObj = user_auth_cmdb.objects.filter(group_name__uuid__in=auth_group_uuid_list).values()
            # print(uacObj)
            # 如果检查到不符合的权限组,返回错误页
            # print(view_name)
            # print(uacObj)
            for i in uacObj:
                if i[view_name]:
                    # print(i,i[view_name])
                    return func(request,*args,**kwargs)
            return redirect("error_auth")
        return auth
    return decorator


def get_node_list(request):
    '''
    获取用户主机权限
    :param request:
    :return:
    '''
    email = request.session.get('email')
    userObj = CustomUser.objects.get(email=email)
    server_all = Server.objects.filter(is_active=True)
    # 如果是超级管理员不检查
    if userObj.is_superuser:
       return server_all
    server_all = server_all.filter(Q(authnode_node__user_name=userObj.uuid)|Q(authdepnode_node__department_name=userObj.department))
    return server_all




