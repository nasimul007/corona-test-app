from django.conf.urls import url
from .views import *

urlpatterns = [
    # user
    url(r'^list', UserManagementView.as_view(), name='list'),
    url(r'^add_user', AddUser.as_view(), name='add_user'),
    url(r'^edit_user/(?P<pk>[0-9]+)/$', EditUser.as_view(), name='edit_user'),
    # role
    url(r'^role_list', RoleList.as_view(), name='role_list'),
    # department
    url(r'^department', department.as_view(), name='departments'),
    # branch
    url(r'^branch', branch.as_view(), name='branch'),
    # Group
    url(r'^group_list', GroupList.as_view(), name='group_list'),
]
