from datetime import datetime

# 生成通用编码工具类
from gcxl_apps.gcxl import models


class CreateCommonCodeUtils(object):
    @classmethod
    def create_code(cls, mode, prefix):
        """
        生成规则：前缀prefix + 当前时间字符串 + 当前微秒时间戳后三位
        :param mode: 编码类型:COMPANY:客户编码; CONTRACT:合同编码; ORDER:业务编码; ENTER_PLAN: 进场计划; OUT_PLAN: 出场计划
        :param prefix: 前缀 YI:进口; YE:出口
        :return:
        """
        try:
            # 当前系统日期
            current_year = datetime.now().year
            current_month = datetime.now().month
            data = {}
            serial_number_list = models.SerialNumber.objects.filter(mode=mode, prefix=prefix).order_by('-suffix')
            suffix = 10000
            if serial_number_list.count() > 0:
                suffix_int = serial_number_list[0].suffix
                suffix = suffix_int + 1
                suffix_str = str(suffix)[1:]
            else:
                suffix_str = '0000'
            code = prefix + str(current_year) + str(current_month) + suffix_str

            data['prefix'] = prefix
            data['mid_date'] = str(current_year) + str(current_month)
            data['suffix'] = suffix
            data['mode'] = mode
            data['create_user'] = 'admin'

            models.SerialNumber.objects.create(**data)

        except Exception as e:
            print('生成编码失败！！！')
            print(e)
            code = '-100'
        return code


class UserInfoUtils(object):

    @classmethod
    def get_user(cls, request):
        """
        :param request: 业务请求参数
        :return:
        """
        try:
            bearer_token = request.headers._store.get('authorization')[1]
            token = bearer_token.split()[1]
            obj = models.UserToken.objects.filter(token=token).first()
            if obj is None:
                return '-502'
            user = models.User.objects.get(id=obj.user_id)
            return user

        except Exception as e:
            print(e)
            message = '获取用户信息有误！'
        return message
