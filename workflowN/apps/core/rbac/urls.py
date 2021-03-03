from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('role', RoleViewSet, base_name='role')
router.register('permission', PermissionViewSet, base_name='permission')
router.register('user', UserViewSet, base_name='user')
router.register('delegate', DelegateViewSet, base_name='delegate')
router.register('group', GroupViewSet, base_name='group')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^upload_report_download/', upload_report_download, name='upload_report_download'),
]
