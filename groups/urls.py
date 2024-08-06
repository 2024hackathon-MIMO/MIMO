from django.urls import path
from .views import *

app_name = 'groups'

urlpatterns = [
    path('my_groups/', my_groups, name='my_groups'),
    path('group_detail/<int:group_id>/', group_detail, name='group_detail'),
    path('group_list/', group_list, name='group_list'),
    path('group_create/', group_create, name='group_create'),
    path('join_group/<int:group_id>/', join_group, name='join_group'),
    #검색 기능 뷰 추가
    path('search/', search, name='search'),
    # 10:25추가
    path('my_group_detail/<int:group_id>/', mygroup_detail, name = 'my_group_detail'),
]