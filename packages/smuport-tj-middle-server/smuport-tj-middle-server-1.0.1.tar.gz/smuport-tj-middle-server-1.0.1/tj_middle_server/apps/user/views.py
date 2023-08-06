# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as DrfFilters
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework_simplejwt.views import TokenObtainPairView

from . import filters
from . import models
from . import serializers
from ..utils.yeahModalViewSet import yeahModalViewSet
from ..utils.pager import MyPageNumberPagination
from ..utils.response import CommonResponseMixin, ReturnCode


class UserManageViewSet(yeahModalViewSet, CommonResponseMixin):
    # put在data里放id， delete在url拼接id，别忘了/结尾，不然会重定向到get
    queryset = models.User.objects.filter(is_active=True).order_by('username')
    serializer_class = serializers.UserManageSerializer

    # 第一种 自定filter类写法
    # filter_backends = (DjangoFilterBackend,)
    # filter_class = DepartmentFilter

    # 第二种 字段模糊搜索， url的key必须为search写法
    filter_backends = (DrfFilters.SearchFilter,)
    search_fields = ('name', 'username', 'department__name', 'role__title')

    pagination_class = MyPageNumberPagination  # 分页

    def create(self, request, *args, **kwargs):
        """
        :param request: username, password, email, name, department_id, role_id
        :param args:
        :param kwargs:
        :return:
        """
        try:
            data = json.loads(request.body.decode())
            username = data['username']
            email = data['email']
            password = data['password']
            department_id = data.get('department_id')
            role = models.Role.objects.get(id=data['role_id'])
            extra_fields = {}
            if department_id is not None:
                department_obj = models.Department.objects.get(id=department_id)
                extra_fields['department'] = department_obj
            extra_fields['role'] = role
            extra_fields['name'] = data['name']
            extra_fields['is_staff'] = True
            extra_fields['is_active'] = True

            models.User.objects.create_user(username, email, password, **extra_fields)
            response = self.wrap_json_response(code=1000, message="用户创建成功！")
        except Exception as e:
            print(e)
            response = self.wrap_json_response(code=1002, message="用户创建失败！")
        return Response(response)

    def destroy(self, request, *args, **kwargs):
        """
        删除数据，需要url后面拼接id，不能忘了/结尾，不然会重定向到get请求
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        try:
            instance = self.get_object()
            instance.is_active = False
            instance.save()
            response = self.wrap_json_response()

        except Exception as e:
            print(e)
            response = self.wrap_json_response(code=1002, message="删除资料失败，请检查错误！")

        return Response(response)

    def put(self, request, *args, **kwargs):
        """
        更新用户资料
        :param request: vessel对象
        :param args:
        :param kwargs:
        :return: err_code: 返回状态码； message：状态提示
        """
        try:
            update_user = json.loads(request.body.decode())
            id = update_user["id"]

            department_id = update_user.get('department')
            if department_id is not None:
                department_obj = models.Department.objects.get(id=department_id)
                update_user['department'] = department_obj
            else:
                update_user['department'] = ''

            user_password = update_user['password']
            models.User.set_password(user_password)
            del update_user['password']

            role_id = update_user['role']
            role_obj = models.Role.objects.get(id=role_id)
            update_user['role'] = role_obj

            user_obj = models.User.objects.filter(id=id)
            user_obj.update(**update_user)
            response = self.wrap_json_response()

        except Exception as e:
            print(e)
            response = self.wrap_json_response(code=1002, message="更新用户资料失败，请检查错误！")

        return Response(response)


class LoginView(TokenObtainPairView, CommonResponseMixin):
    """
    登录视图
    """

    def post(self, request, *args, **kwargs):
        user_info = {
            'password': request.data['password'],
            'username': request.data['username']
        }
        serializer = self.get_serializer(data=user_info)
        try:
            serializer.is_valid(raise_exception=True)  # 验证序列化的合法性，如果出错跑出异常
            name = models.User.objects.get(username=user_info['username']).username
            id = models.User.objects.get(username=user_info['username']).id
            serializer.validated_data['name'] = name
            serializer.validated_data['id'] = id
            response = self.wrap_json_response(data=serializer.validated_data)

        except Exception as e:
            print(e)
            response = self.wrap_json_response(code=ReturnCode.UNAUTHORIZED, message="用户名或密码错误，请重新登录")

        return Response(response)


class DepartmentViewSet(yeahModalViewSet, CommonResponseMixin):
    # put在data里放id， delete在url拼接id，别忘了/结尾，不然会重定向到get
    queryset = models.Department.objects.filter(if_deleted=False).order_by('name')
    serializer_class = serializers.DepartmentSerializers

    # 第一种 自定filter类写法
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.DepartmentFilter

    # 第二种 字段模糊搜索， url的key必须为search写法
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('engName', 'chiName')

    pagination_class = MyPageNumberPagination  # 分页

    # 重写更新函数
    def put(self, request, *args, **kwargs):
        """
        更新科目
        :param request:  department对象（需要id）
        :param args:
        :param kwargs:
        :return: err_code: 返回状态码； message：状态提示
        """
        try:
            data = json.loads(request.body.decode())
            department_object = models.Department.objects.filter(id=data['id'])
            department_object.update(**data)
            response = self.wrap_json_response()

        except Exception as e:
            print(e)
            response = self.wrap_json_response(code=1002, message="更新部门信息失败，请检查错误！")

        return Response(response)


class RoleViewSet(yeahModalViewSet, CommonResponseMixin):
    # put在data里放id， delete在url拼接id，别忘了/结尾，不然会重定向到get
    queryset = models.Role.objects.filter().order_by('title')
    serializer_class = serializers.RoleSerializer

    # 第一种 自定filter类写法
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.RoleFilter

    # 第二种 字段模糊搜索， url的key必须为search写法
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('engName', 'chiName')

    pagination_class = MyPageNumberPagination  # 分页



