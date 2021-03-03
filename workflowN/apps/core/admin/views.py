from django import forms
from django.forms.models import ModelForm, modelform_factory
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from apps.workflow.bpmn.models import Weekend, Holiday
from conf import settings


def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[-1].strip()
    else:
        ip_address = request.META.get('REMOTE_ADDR')

    return ip_address


@property
def admin_sidebar_menu(self):
    sidebar = []
    user_management_menu = [
        ['allowed', 'Users', reverse_lazy('admin:user:list'), 'zmdi-accounts-list-alt', []],
        ['allowed', 'Groups', reverse_lazy('admin:user:group_list'), 'zmdi-accounts', []],
        ['allowed', 'Roles', reverse_lazy('admin:user:role_list'), 'zmdi-account-box', []]
    ]

    if settings.WORKFLOW == 'aBX3RODumf':
        user_management_menu.append(
            ['allowed', 'Departments', reverse_lazy('admin:user:departments'), 'zmdi-markunread-mailbox', []])

        user_management_menu.append(
            ['allowed', 'Branches', reverse_lazy('admin:user:branch'), 'zmdi-pin-account', []])

    if self.request.user.role.id == 1:
        sidebar.append(['allowed', 'User Management', '#', 'zmdi-pin-account', user_management_menu])

        settings_sub_menu = [['allowed', 'Mail', reverse_lazy('admin:mail:view'), 'zmdi-email', []]]

        if settings.WORKFLOW == 'aBX3RODumf':
            settings_sub_menu.append(['allowed', 'Process Categories', reverse_lazy('admin:category:view'),
                                      'zmdi-format-list-bulleted',
                                      []])

            settings_sub_menu.append(['allowed', 'Weekends and holidays', reverse_lazy('admin:weekend_holiday'),
                                      'zmdi-calendar',
                                      []])

        if settings.DMS == '9dL53eBFDK':
            settings_sub_menu.append(['allowed', 'Restore Data', reverse_lazy('dms:dms_restore:restore'),
                                      'zmdi-time-restore-setting',
                                      []])
            sidebar.append(['allowed', 'Categorization', reverse_lazy('dms:document:list'), 'zmdi-group', []])
        sidebar.append(['allowed', 'Settings', '#', 'zmdi-settings', settings_sub_menu])

        sidebar.append(
            ['allowed', 'Announcement', reverse_lazy('admin:announcement:view'), 'zmdi-surround-sound', []]
        )

        if settings.WORKFLOW == 'aBX3RODumf':
            sidebar.append(
                ['allowed', 'Overall Monitor', reverse_lazy('admin:overall_monitor'), 'zmdi-format-list-bulleted', []],
            )
            sidebar.append(
                ['allowed', 'Workflow Design', reverse_lazy('admin:designer:project_list'), 'zmdi-brush', []],
            )

    else:
        perm_list = self.request.session.get('permission_list')

        if 1 in perm_list:
            sidebar.append(['allowed', 'User Management', '#', 'zmdi-pin-account', user_management_menu])

        if 23 in perm_list:
            settings_sub_menu = [['allowed', 'Mail', reverse_lazy('admin:mail:view'), 'zmdi-email', []]]

            if settings.WORKFLOW == 'aBX3RODumf':
                settings_sub_menu.append(['allowed', 'Process Categories', reverse_lazy('admin:category:view'),
                                          'zmdi-format-list-bulleted',
                                          []])

                settings_sub_menu.append(['allowed', 'Weekends and holidays', '#',
                                          'zmdi-calendar',
                                          []])

            if settings.DMS == '9dL53eBFDK':
                settings_sub_menu.append(['allowed', 'Restore Data', reverse_lazy('dms:dms_restore:restore'),
                                          'zmdi-time-restore-setting',
                                          []])

            sidebar.append(['allowed', 'Settings', '#', 'zmdi-settings', settings_sub_menu])

        if 22 in perm_list:
            sidebar.append(
                ['allowed', 'Announcement', reverse_lazy('admin:announcement:view'), 'zmdi-surround-sound', []])

        if settings.WORKFLOW == 'aBX3RODumf' and 26 in perm_list:
            sidebar.append(
                ['allowed', 'Overall Monitor', reverse_lazy('admin:overall_monitor'), 'zmdi-format-list-bulleted', []],
            )

        if settings.WORKFLOW == 'aBX3RODumf' and 2 in perm_list:
            sidebar.append(
                ['allowed', 'Workflow Design', reverse_lazy('admin:designer:project_list'), 'zmdi-brush', []])

        if settings.DMS == '9dL53eBFDK' and 8 in perm_list:
            sidebar.append(['allowed', 'Categorization', reverse_lazy('dms:document:list'), 'zmdi-group', []])

    return sidebar


class AdminView(TemplateView):
    sidebar_menu = admin_sidebar_menu


class WeekendHoliday(TemplateView):
    sidebar_menu = admin_sidebar_menu
    template_name = 'workflow/weekend_holiday/weekend_holiday.html'

    def get_context_data(self, **kwargs):
        context = super(WeekendHoliday, self).get_context_data(**kwargs)
        context['weekend_form'] = modelform_factory(Weekend, exclude=[])()
        context['holiday_form'] = modelform_factory(Holiday, exclude=[])()
        context['weekend_list'] = list(Weekend.objects.all().values_list('day', flat=True))
        context['holiday_list'] = list(Holiday.objects.all().values_list('date', flat=True))

        return context


class OverallMonitorView(TemplateView):
    sidebar_menu = admin_sidebar_menu
    overall = 'y'
    template_name = 'workflow/cases/monitor.html'
