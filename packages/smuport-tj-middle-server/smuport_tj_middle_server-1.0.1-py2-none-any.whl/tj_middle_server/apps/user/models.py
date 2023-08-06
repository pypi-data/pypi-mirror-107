from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.


# 角色表
class Role(models.Model):
    title = models.CharField(max_length=32, unique=True, verbose_name="角色名称")
    code = models.CharField(max_length=20, unique=True, verbose_name="角色代码")
    mark = models.CharField(max_length=32, null=True, blank=True, verbose_name="备注")

    class Meta:
        db_table = 'role'
        verbose_name_plural = '角色表'

    def __str__(self):
        return self.id


# 部门表
class Department(models.Model):
    name = models.CharField(max_length=60, null=True, blank=True, verbose_name="部门名称")
    no = models.CharField(max_length=20, null=True, blank=True, verbose_name="编号")
    instruction = models.CharField(max_length=500, null=True, blank=True, verbose_name="说明")
    if_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    company_leader = models.CharField(default='', max_length=10, verbose_name="分管部门领导id")

    class Meta:
        verbose_name = "部门表"
        verbose_name_plural = verbose_name
        db_table = "department"

    def __str__(self):
        return self.id


# 用户表
class User(AbstractUser):
    department = models.ForeignKey(Department, related_name='user', null=True, blank=True, on_delete=models.CASCADE,
                                   verbose_name="所属部门")
    name = models.CharField(default='admin', max_length=10, verbose_name="用户名")
    gender = models.CharField(choices=(('0', '男'), ('1', '女')), null=True, blank=True, max_length=1, verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    role = models.ForeignKey(Role, default='1', related_name='user', on_delete=models.CASCADE, verbose_name="用户角色")

    class Meta:
        verbose_name = "用户信息表"
        verbose_name_plural = verbose_name
        db_table = "user"

    def __str__(self):
        return self.name


# 供应商表
class Supplier(models.Model):
    name = models.CharField(max_length=40, verbose_name="供应商名称")
    mobile = models.CharField(max_length=20, null=True, blank=True, verbose_name="联系电话")
    address = models.CharField(max_length=60, null=True, blank=True, verbose_name="联系地址")
    credit_code = models.CharField(max_length=18, null=True, blank=True, verbose_name="企业信用代码")

    class Meta:
        verbose_name = "供应商表"
        verbose_name_plural = verbose_name
        db_table = "supplier"

    def __str__(self):
        return self.name

