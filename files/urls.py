from django.urls import path,re_path

from files import views


urlpatterns = [
    re_path(r'list/',views.file_list,name='file_list'),
    re_path('^upload/', views.upload_file,name='upload'),
    re_path('^download/', views.upload_file,name='download'),

]



