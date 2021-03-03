import random
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey



def unique_id():
    return random.randint(1, 9999999999)


class Department(MPTTModel):
    name = models.CharField(max_length=50)

    manager = models.ForeignKey('rbac.User', null = True, related_name='manager')

    active = models.BooleanField(default=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Branch(MPTTModel):
    name = models.CharField(max_length=50)

    active = models.BooleanField(default=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    number = models.CharField(null=False, blank=False, default=unique_id, max_length=100)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name