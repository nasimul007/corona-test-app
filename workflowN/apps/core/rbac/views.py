import operator
import re
from collections import OrderedDict
from functools import reduce
from django.utils.dateparse import parse_date
from datetime import datetime
from django.db.models import Q, Count
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from django.http import HttpResponse
from apps.core.admin.views import get_ip_address
from apps.core.api.Pagination import LargeResultsSetPagination
from apps.core.api.viewset import CustomViewSetForQuerySet
from apps.core.api.validators import UniqueNameValidator
from apps.core.api.permission import GreenOfficeApiBasePermission

from apps.core.rbac.models import User, Role, Permission, Group, UserDelegate
from apps.dms.api.dms_activity.models import DmsActivity
from django.utils import timezone
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage


class AuditTrail:
    def __init__(self, current_user, user_info, remote_addr, operation, operation_name):
        self.current_user = current_user
        self.user_info = user_info
        self.remote_addr = remote_addr
        self.operation = operation
        self.operation_name = operation_name

    def add_audit(self):
        user_id = self.current_user.id
        user_name = self.user_info.get_full_name()
        ip = self.remote_addr
        activity_time = timezone.now()
        operation = self.operation
        description = "User: '" + user_name + "' has been " + self.operation_name + \
                      " with Role: '" + self.user_info.role.name + "'"
        DmsActivity(user_id=user_id, operation=operation, ip=ip, description=description,
                    activity_time=activity_time).save()


class DelegateSerializer(serializers.ModelSerializer):
    user_in_action_name = serializers.StringRelatedField(source='present_user.get_full_name')
    user_in_action_id = serializers.StringRelatedField(source='present_user.pk')

    class Meta:
        model = UserDelegate
        fields = ['id', 'user_in_action_name', 'user_in_action_id', 'start_date', 'end_date']


class DelegateViewSet(CustomViewSetForQuerySet):
    permission_classes = [GreenOfficeApiBasePermission]
    serializer_class = DelegateSerializer
    model = UserDelegate
    permission_id = [3, 25, ]

    def create(self, request, *args, **kwargs):
        if request.data.get('is_edit') is None or not request.data.get('is_edit'):
            raise serializers.ValidationError({'detail': 'Please indicate if it is an edit or create delegatee'})
        else:
            isEdit = request.data.get('is_edit')
            if isEdit == "1":
                delegation_id = self.request.data.get('delegation_id')
                if delegation_id is None or not delegation_id:
                    raise serializers.ValidationError({'detail': 'You must provide a delegation_id for edit operation'})
                detail = self.model.objects.get(pk=delegation_id)
                if detail.is_active == 0:
                    raise serializers.ValidationError({'detail': 'This delegation id is already expired. '
                                                                 'you cannot edit this id'})
                from_user = detail.absent_user
                to_user = User.objects.get(pk=self.request.data.get('to_duty', detail.present_user.pk))
                start_date = self.request.data.get('activation_date', None)
                end_date = self.request.data.get('expiry_date', None)
                if start_date is None:
                    start_date_date = detail.start_date
                else:
                    start_date = start_date.replace("/", "-")
                    start_date_date = parse_date(start_date)
                if end_date is None:
                    end_date_date = detail.end_date
                else:
                    end_date = end_date.replace("/", "-")
                    end_date_date = parse_date(end_date)
                if end_date_date < start_date_date:
                    raise serializers.ValidationError(
                        {'detail': 'Invalid Expiry date'})
                if detail.present_user == to_user and detail.start_date == start_date_date and detail.end_date == end_date_date:
                    raise serializers.ValidationError({'detail': 'No new information to edit'})
                detail.is_active = 0
                detail.save()
            else:
                if request.data.get('from_duty') is None or not request.data.get('from_duty'):
                    raise serializers.ValidationError({'detail': 'Please provide the from_duty user id.'})

                if request.data.get('to_duty') is None or not request.data.get('to_duty'):
                    raise serializers.ValidationError({'detail': 'Please provide the to_duty user id.'})

                if request.data.get('activation_date') is None or not request.data.get('activation_date'):
                    raise serializers.ValidationError({'detail': 'Please provide the activation_date.'})

                if request.data.get('expiry_date') is None or not request.data.get('expiry_date'):
                    raise serializers.ValidationError({'detail': 'Please provide the expiry_date.'})
                try:
                    from_user = User.objects.get(pk=request.data.get('from_duty'))
                except User.DoesNotExist:
                    raise serializers.ValidationError({'detail': 'No user with from_duty user id exists'})
                try:
                    to_user = User.objects.get(pk=request.data.get('to_duty'))
                except User.DoesNotExist:
                    raise serializers.ValidationError({'detail': 'No user with to_duty user id exists'})
                start_date = request.data.get('activation_date')
                if "/" not in start_date:
                    raise serializers.ValidationError({'detail': 'Please provide a valid format of activation_date (yyyy/mm/dd)'})
                start_date = start_date.replace("/", "-")
                start_date_date = parse_date(start_date)
                end_date = request.data.get('expiry_date')
                if "/" not in end_date:
                    raise serializers.ValidationError({'detail': 'Please provide a valid format of expiry_date (yyyy/mm/dd)'})
                end_date = end_date.replace("/", "-")
                end_date_date = parse_date(end_date)
                already_assigned = self.model.objects.filter(absent_user=from_user, is_active=1).order_by('-id')[:1]
                if already_assigned.exists():
                    raise serializers.ValidationError({'detail': 'You have already one delegatee assigned.'})
                else:
                    if end_date_date < start_date_date:
                        raise serializers.ValidationError({'detail': 'Invalid Expiry date'})
        if datetime.now().date() < start_date_date:
            is_active = -1
        else:
            is_active = 1
        added_delegatee = self.model(is_active=is_active, absent_user=from_user, present_user=to_user,
                                     start_date=start_date_date, end_date=end_date_date)
        added_delegatee.save()
        queryset = self.model.objects.filter(pk=added_delegatee.pk)
        serializer = self.get_serializer(list(queryset), many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        if user_id and user_id is not None:
            queryset = self.model.objects.filter(~Q(is_active=0), absent_user__pk=user_id).order_by('-id')[:1]
            to_be_deleted = []
            for q in queryset:
                if q.is_expired:
                    q.is_active = 0
                    q.save()
                    to_be_deleted.append(q.id)
                if q.is_active:
                    q.is_active = 1
                    q.save()
            if len(to_be_deleted):
                queryset.filter(id__in=to_be_deleted).delete()
            serializer = self.get_serializer(list(queryset), many=True)
            return Response(serializer.data)
        else:
            return Response({'detail': 'You must provide a user_id for delegation query'},
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            delete_instance = self.model.objects.get(pk=kwargs['pk'])
        except self.model.DoesNotExist:
            raise serializers.ValidationError({'detail': 'No row found with this id'})
        if delete_instance.is_active == 0:
            raise serializers.ValidationError({'detail': 'This delegation id is already expired. '
                                                         'you cannot delete this id'})
        delete_instance.is_active = 0
        delete_instance.save()
        return Response({'detail': 'Your Delegatee has been deleted successfully.'}, status=status.HTTP_200_OK)


class DelegateUserSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(source='get_full_name')
    id = serializers.StringRelatedField(source='pk')

    class Meta:
        model = User
        fields = ['name', 'id']


class UserSerializer(serializers.ModelSerializer):
    slug_regex = re.compile(r'^[-a-zA-Z0-9_.]{4,50}$')

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())], required=True)
    username = serializers.RegexField(validators=[UniqueNameValidator(queryset=User.objects.all(), lookup='iexact')],
                                      regex=slug_regex,
                                      error_messages={
                                          'invalid': 'Username can contain alphanumeric, underscore and period(.). '
                                                     'Length: 4 to 50'
                                      })
    is_active = serializers.BooleanField(default=True)
    role_name = serializers.ReadOnlyField(source='role.name')
    group = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        exclude = ['user_permissions', 'is_superuser', 'groups']
        read_only_fields = ('id', 'date_joined')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        operation = "Create User"
        operation_name = "Created"
        x_forwarded_for = self.context['request'].META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[-1].strip()
        else:
            ip_address = self.context['request'].META.get('REMOTE_ADDR')
        AuditTrail(self.context['request'].user, user, ip_address,
                   operation, operation_name).add_audit()
        return user

    def update(self, instance, validated_data):
        skip_list = ['is_active', 'is_superuser', 'position',
                     'status', 'replaced_by', 'expiry_date', 'role_id']
        for attr, value in validated_data.items():
            if instance.id == 1 and attr in skip_list:
                continue
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        # Dms Activity
        description = "User: '" + instance.get_full_name() + "' has been Updated"
        x_forwarded_for = self.context['request'].META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[-1].strip()
        else:
            ip_address = self.context['request'].META.get('REMOTE_ADDR')
        DmsActivity(user=self.context['request'].user, operation="Update User",
                    ip=ip_address,
                    description=description, activity_time=timezone.now()).save()
        return instance


class UserViewSet(CustomViewSetForQuerySet):
    permission_classes = [GreenOfficeApiBasePermission]
    serializer_class = UserSerializer
    pagination_class = LargeResultsSetPagination
    model = User
    change_keys = {
        'role_name': 'role__name',
        'username': 'username',
    }
    search_keywords = ['username', 'first_name',
                       'last_name', 'email', 'role__name', 'status']
    permission_id = [1, 3, 25, ]

    def list(self, request, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        if user_id and user_id is not None:
            self.serializer_class = DelegateUserSerializer
            queryset = self.model.objects.exclude(pk=user_id)
            serializer = self.get_serializer(list(queryset), many=True)

        else:
            queryset = self.model.objects.all()
            search = self.request.query_params.get('search[value]', None)
            column_id = self.request.query_params.get('order[0][column]', None)

            # search
            if search and search is not None and self.search_keywords is not None:
                search_logic = []

                for entity in self.search_keywords:
                    search_logic.append(Q(**{entity + '__icontains': search}))

                queryset = queryset.filter(reduce(operator.or_, search_logic))

            # ascending or descending order
            if column_id and column_id is not None:
                column_name = self.request.query_params.get(
                    'columns[' + column_id + '][data]', None)

                if self.change_keys is not None:
                    for key in self.change_keys:
                        if column_name == key:
                            column_name = self.change_keys.get(key)

                if column_name != '':
                    order_dir = '-' if self.request.query_params.get(
                        'order[0][dir]') == 'desc' else ''
                    queryset = queryset.order_by(order_dir + column_name)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.id == 1:
            return Response(OrderedDict([
                ('detail', 'Superuser deleting prohibited.')
            ]), status=status.HTTP_403_FORBIDDEN)

        # Audit Trail
        operation = "Delete User"
        description = "User: " + instance.get_full_name() + " has been Deleted"
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[-1].strip()
        else:
            ip_address = self.request.META.get('REMOTE_ADDR')
        DmsActivity(user=self.request.user, operation=operation, ip=ip_address,
                    description=description, activity_time=timezone.now()).save()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoleSerializer(serializers.ModelSerializer):
    active = serializers.BooleanField(default=True)
    code = serializers.RegexField(required=True,
                                  regex=re.compile(r'^[a-zA-Z0-9_]+$'),
                                  validators=[UniqueValidator(queryset=Role.objects.all())])
    permission_name = serializers.StringRelatedField(
        source='permission', many=True, read_only=True)
    user_count = serializers.StringRelatedField(
        source='user.count', read_only=True)

    class Meta:
        model = Role
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'modified_at')


class RoleViewSet(CustomViewSetForQuerySet):
    permission_classes = [GreenOfficeApiBasePermission]
    serializer_class = RoleSerializer
    pagination_class = LargeResultsSetPagination
    model = Role
    change_keys = {
        'permission_name': 'permission__name',
        'user_count': 'user',
    }
    search_keywords = ['name']
    permission_id = [1, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Audit Trail
        permissions = serializer.data['permission_name']
        permission = ', '.join(permissions)
        description = "Role: '" + serializer.data['name'] + "' has been created with the permission of: " + permission
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[-1].strip()
        else:
            ip_address = self.request.META.get('REMOTE_ADDR')
        DmsActivity(user=self.request.user, operation="Role Added", ip=ip_address,
                    description=description, activity_time=timezone.now()).save()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        if int(self.kwargs.get('pk')) == 1:
            return Response({
                'errors': 'You can not update the detail of this role.'
            }, status=404)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance = self.get_object()
            serializer = self.get_serializer(instance)

        description = "Role: {} has been updated.".format(instance.name)

        DmsActivity(user=self.request.user, operation="Role Updated", ip=get_ip_address(request),
                    description=description, activity_time=timezone.now()).save()
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.id == 1:
            return Response({
                'errors': 'You can not delete this role.'
            }, 404)

        user = instance.user.count()

        if user > 0:
            return Response({
                'errors': 'This role has already {0} user(s).'.format(user)
            }, 404)

        # Audit Trail
        description = "Role: '" + instance.name + "' has been Deleted"
        DmsActivity(user=self.request.user, operation="Role Delete", ip=get_ip_address(request),
                    description=description, activity_time=timezone.now()).save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        if self.model is None:
            raise AssertionError('CustomViewSetForQuerySet need to include a model')

        queryset = self.model.objects.filter()
        search = self.request.query_params.get('search[value]', None)
        column_id = self.request.query_params.get('order[0][column]', None)

        # search
        if search and search is not None and self.search_keywords is not None:
            search_logic = []
            print(search)

            for entity in self.search_keywords:
                search_logic.append(Q(**{entity + '__icontains': search}))

            queryset = queryset.filter(reduce(operator.or_, search_logic))

        # ascending or descending order
        if column_id and column_id is not None:

            column_name = self.request.query_params.get('columns[' + column_id + '][data]', None)
            print(column_name)

            if self.change_keys is not None:
                for key in self.change_keys:
                    if column_name == key:
                        column_name = self.change_keys.get(key)

            if column_name != '':
                order_dir = '-' if self.request.query_params.get('order[0][dir]') == 'desc' else ''
                if column_name == 'user_count':
                    print("ok")
                else:
                    queryset = queryset.order_by(order_dir + column_name).annotate(total=Count('user')).order_by(
                        order_dir + 'total')

        return queryset


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class PermissionViewSet(CustomViewSetForQuerySet):
    permission_classes = [GreenOfficeApiBasePermission]
    serializer_class = PermissionSerializer
    pagination_class = LargeResultsSetPagination
    model = Permission
    search_keywords = ['name']
    permission_id = [1, ]

    def get_queryset(self):
        if self.model is None:
            raise AssertionError(
                'CustomViewSetForQuerySet need to include a model')
        queryset = self.model.objects.filter().order_by('name')

        return queryset


class GroupSerializer(serializers.ModelSerializer):
    slug_regex = re.compile(r'^[-a-zA-Z0-9_.\s]{2,100}$')

    name = serializers.RegexField(validators=[UniqueNameValidator(queryset=Group.objects.all(), lookup='iexact')],
                                  regex=slug_regex,
                                  error_messages={
                                      'invalid': 'Username can contain alphanumeric, underscore and period(.). '
                                                 'Length: 2 to 100'
                                  })

    user_detail = serializers.StringRelatedField(
        source='user', many=True, read_only=True)

    class Meta:
        model = Group
        fields = '__all__'


class GroupViewSet(CustomViewSetForQuerySet):
    permission_classes = [GreenOfficeApiBasePermission]
    model = Group
    serializer_class = GroupSerializer
    pagination_class = LargeResultsSetPagination
    change_keys = {
        'user_detail': 'user__username',
        'user': 'user',
    }
    search_keywords = ['name']
    permission_id = [1, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Audit Trail
        description = "Role: '" + serializer.data['name'] + "' has been Created"
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[-1].strip()
        else:
            ip_address = self.request.META.get('REMOTE_ADDR')
        DmsActivity(user=self.request.user, operation="Group Create", ip=ip_address,
                    description=description, activity_time=timezone.now()).save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # refresh the instance from the database.
            instance = self.get_object()
            serializer = self.get_serializer(instance)

        # Audit Trail
        users = serializer.data['user_detail']
        user = ','.join(users)
        status = "Active" if serializer.data['status'] is True else "Inactive"
        description = "Group: '" + instance.name + "' has been Updated where users are: " + \
                      user + " and Status: " + status
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[-1].strip()
        else:
            ip_address = self.request.META.get('REMOTE_ADDR')
        DmsActivity(user=self.request.user, operation="Group Update", ip=ip_address,
                    description=description, activity_time=timezone.now()).save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user.count()

        if user > 0:
            return Response({
                'errors': 'This group has already {0} user(s).'.format(user)
            }, 404)
        self.perform_destroy(instance)

        # Audit Trail
        description = "Group: '" + instance.name + "' has been Deleted"
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[-1].strip()
        else:
            ip_address = self.request.META.get('REMOTE_ADDR')
        DmsActivity(user=self.request.user, operation="Group Delete", ip=ip_address,
                    description=description, activity_time=timezone.now()).save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        if self.model is None:
            raise AssertionError(
                'CustomViewSetForQuerySet need to include a model')

        queryset = self.model.objects.filter()
        search = self.request.query_params.get('search[value]', None)
        column_id = self.request.query_params.get('order[0][column]', None)

        # ascending or descending order
        if column_id and column_id is not None:
            column_name = self.request.query_params.get(
                'columns[' + column_id + '][data]', None)

            if self.change_keys is not None:
                for key in self.change_keys:
                    if column_name == key:
                        column_name = self.change_keys.get(key)

            if column_name != '':
                order_dir = '-' if self.request.query_params.get(
                    'order[0][dir]') == 'desc' else ''

                if column_name == 'user':
                    queryset = queryset.order_by(order_dir + column_name).annotate(total=Count('user')).order_by(
                        order_dir + 'total')
                else:
                    queryset = queryset.order_by(order_dir + column_name)

        # search
        if search and search is not None and self.search_keywords is not None:
            search_logic = []

            for entity in self.search_keywords:
                search_logic.append(Q(**{entity + '__icontains': search}))

            queryset = queryset.filter(reduce(operator.or_, search_logic))

        return queryset


@api_view(['GET'])
def upload_report_download(request):
    file_name = request.query_params.get('link', None)
    file_path = request.query_params.get('file_path', None)
    print('file_name', file_name)
    print('file_path', file_path)
    if default_storage.exists(file_path):
        response = HttpResponse(default_storage.open(file_path).read())
        filename = file_name.replace(' ', '-').lower()
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        return response
