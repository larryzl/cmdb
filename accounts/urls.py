from django.urls import path,re_path

from accounts import views,user_edit


urlpatterns = [
    re_path('^user/list', views.user_list,name='user_list'),
    re_path('^user/add', views.register,name='user_add'),

    re_path(r'^user/edit/(?P<uid>[\w|\-]+)/$',user_edit.user_edit,name='user_edit'),

    re_path('^user/del/$', views.user_del,name='user_del'),
    re_path('^user/active/$',views.user_active,name='user_active'),

    re_path('^register/$',views.register,name='reggister'),

    re_path('^login/$',views.user_login,name='login'),
    re_path('^logout/$',views.Logout,name='logout'),

    re_path(r'^adduser/$',views.register,name='adduser'),

    re_path(r'^department/list',views.department_list,name='department_list'),
    re_path(r'^department/add$',views.department_add,name='department_add'),
    re_path('^department/edit/(?P<id>\d+)/',views.department_edit,name='department_edit'),
    re_path(r'^department/del/(?P<sid>\w+)',views.department_del,name='department_del'),

]

