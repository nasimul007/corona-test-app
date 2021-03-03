from django.conf.urls import url, include
from apps.core.admin.views import WeekendHoliday, OverallMonitorView

urlpatterns = [
    # core
    url(r'^user/', include('apps.core.user_management.urls', 'user')),
    url(r'^announcement/', include('apps.core.announcement.urls', 'announcement')),
    url(r'^mail/', include('apps.core.mail.urls', 'mail')),

    # workflow
    url(r'^designer/', include('apps.workflow.bpmn.urls', 'designer')),
    url(r'^category/', include('apps.workflow.category.urls', 'category')),
    url(r'^weekend_holiday/', WeekendHoliday.as_view(), name='weekend_holiday'),
    url(r'^overall_monitor/', OverallMonitorView.as_view(), name='overall_monitor'),


    # dms
    url(r'^restore/', include('apps.dms.restore.urls', 'dms_restore')),

]
