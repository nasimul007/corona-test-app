from __future__ import unicode_literals
from datetime import datetime
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from apps.dms.api.department.models import Department, Branch
from .manager import UserManager


class Permission(models.Model):
    name = models.CharField(max_length=50, blank=False,
                            null=False, unique=True)
    code = models.CharField(max_length=50, blank=False, unique=True)
    active = models.BooleanField()

    def __str__(self):
        return '{}'.format(self.name)


class Role(models.Model):
    name = models.CharField(max_length=50, blank=False,
                            null=False, unique=True)
    code = models.CharField(max_length=50, blank=False, unique=True)
    active = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    permission = models.ManyToManyField(Permission, related_name='permissions')

    def __str__(self):
        return self.name


def default_expiry_date():
    return timezone.now() + timezone.timedelta(days=21914.5319)


def avatar_dir(instance, filename):
    return 'avatars/{}/{}'.format(instance.username, filename)


def signature_dir(instance, filename):
    return 'signatures/{}/{}'.format(instance.username, filename)


status_choices = (
    ('0', 'Inactive'),
    ('1', 'Active'),
    ('2', 'Vacation'),
    ('3', 'Expired'),
)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('email address'), unique=True, null=False, blank=False)
    username = models.CharField(_('user name'), max_length=50,
                                unique=True,
                                null=False,
                                blank=False,
                                validators=[RegexValidator(
                                    regex='[-a-zA-Z0-9_.]{4,50}$',
                                    message='Username contains alphanumeric, underscore and period(.). Length: 4 to 50'
                                )])
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=30, blank=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    avatar = models.ImageField(upload_to=avatar_dir, null=True, blank=True)
    signature = models.ImageField(upload_to=signature_dir, null=True, blank=True)
    address = models.CharField(max_length=120, blank=True)
    phone_number = models.CharField(blank=False, max_length=14, null=False)
    position = models.CharField(max_length=50, blank=True, null=True)
    expiry_date = models.DateTimeField(
        default=default_expiry_date, null=False, blank=False)
    status = models.CharField(choices=status_choices, max_length=50, default=1)
    role = models.ForeignKey(
        Role, on_delete=models.PROTECT, null=False, blank=False, related_name='user', default=2)

    configuration_type = models.IntegerField(choices=(
        (0, 'cannot configure'), (1, 'can configure and DMS'), (2, 'can configure and workflow'),),
        default=0
    )
    department = models.ForeignKey(Department, blank=True, null=True)
    branch = models.ForeignKey(Branch, blank=True, null=True)
    reports_to = models.ForeignKey('self', null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return '%s %s (%s)' % (self.first_name, self.last_name, self.username)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def save(self, *args, **kwargs):
        self.clean()
        super(User, self).save()

    def clean(self):
        if self.username:
            return " ".join(self.username.lower().split())

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '{0} {1}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


class UserDelegate(models.Model):
    is_active = models.IntegerField(null=False, blank=False, choices=((0, 'No'), (1, 'Yes'), (-1, 'Upcoming')))
    absent_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='absent_user')
    present_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='present_user')
    start_date = models.DateField(_('start_date'), null=False, blank=False)
    end_date = models.DateField(_('end_date'), null=False, blank=False)

    def __str__(self):
        return '{} {} {} {} {}'.format(self.is_active,self.absent_user,self.present_user,self.start_date,self.end_date)

    @property
    def is_expired(self):
        if datetime.now().date() > self.end_date:
            return True
        return False

    @property
    def is_delegation_started(self):
        if datetime.now().date() < self.start_date:
            return False
        return True


class Group(models.Model):
    name = models.CharField(max_length=100,
                            blank=False,
                            null=False,
                            unique=True,
                            validators=[RegexValidator(
                                regex='[-a-zA-Z0-9_.\s]{2,100}$',
                                message='Group contains alphanumeric, underscore, space and period(.). Length: 2 to 100'
                            )]
                            )
    status = models.BooleanField(default=True)
    user = models.ManyToManyField(User, blank=True, related_name='group')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.clean()
        super(Group, self).save()

    def clean(self):
        if self.name:
            return " ".join(self.name.split())
