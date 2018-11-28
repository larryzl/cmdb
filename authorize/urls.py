from django.urls import path,re_path

from authorize import views


urlpatterns = [
    re_path('^hrule/list', views.auth_index,name='auth_list'),
    re_path('^hrule/add', views.auth_add,name='hrule_add'),
    re_path('^hrule/edit/(?P<id>[\w|\-]+)/', views.auth_edit,name='hrule_edit'),
    re_path('^hrule/del/', views.auth_del,name='hrule_del'),

    re_path('^hrule/authorize/(?P<id>[\w|\-]+)/',views.auth_group_authorize,name='hrule_authorize'),

    re_path('^arule/index$',views.arule_index,name='arule_index'),  # 主机授权首页

    re_path('^arule/ugrant/list/$',views.arule_user_grant_list,name='arule_user_grant_list'),    # 用户授权列表
    re_path('^arule/ugrant/edit/(?P<uid>[\w|\-]+)/$',views.arule_user_grant,name='arule_user_grant_edit'),    # 用户授权详情

    re_path('^arule/dgrant/list/$',views.arule_depart_grant_list,name='arule_depart_grant_list'),    # 用户授权列表'
    re_path('^arule/dgrant/edit/(?P<uid>[\w|\-]+)/$',views.arule_depart_grant_edit,name='arule_depart_grant_edit'),    # 用户授权列表'







]

