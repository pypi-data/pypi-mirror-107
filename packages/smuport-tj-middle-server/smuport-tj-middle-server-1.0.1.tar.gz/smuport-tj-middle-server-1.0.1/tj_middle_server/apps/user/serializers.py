from rest_framework import serializers
from . import models


class DepartmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = "__all__"


class UserManageSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    role_name = serializers.SerializerMethodField()

    def get_role_name(self, row):
        return row.role.title

    def get_department_name(self, row):
        if row.department:
            return row.department.no
        else:
            return ''

    class Meta:
        model = models.User
        fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = "__all__"
