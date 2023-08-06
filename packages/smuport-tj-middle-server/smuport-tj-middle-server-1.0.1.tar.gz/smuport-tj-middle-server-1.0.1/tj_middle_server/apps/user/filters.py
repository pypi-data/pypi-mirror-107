from django_filters.rest_framework import FilterSet, filters

from . import models


class DepartmentFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    no = filters.CharFilter(field_name='no', lookup_expr='icontains')
    instruction = filters.CharFilter(field_name='instruction', lookup_expr='icontains')
    if_deleted = filters.BooleanFilter(field_name='if_deleted')

    class Meta:
        model = models.Department
        fields = ['name', 'no', 'instruction', 'if_deleted']


class RoleFilter(FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    code = filters.CharFilter(field_name='code', lookup_expr='icontains')
    mark = filters.CharFilter(field_name='mark', lookup_expr='icontains')

    class Meta:
        model = models.Role
        fields = ['title', 'code', 'mark']
