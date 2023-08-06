from rest_framework import viewsets
from rest_framework.response import Response


class yeahModalViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        """
        获取数据，获取单独数据时需要在params添加查询id
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            res = super().list(request, *args, **kwargs)
            response = self.wrap_json_response(data=res.data)
            return Response(response)
        except Exception as e:
            print(e)
            response = self.wrap_json_response(code=1002, message="获取失败，请检查错误！")
            return Response(response)
            # return Response({'errCode': '1002', 'errMessage': '获取失败'})

    def update(self, request, *args, **kwargs):
        """
        更新数据，需要在url后面拼接id
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            res = super().update(request, *args, **kwargs)
            response = self.wrap_json_response()
            return Response(response)
        except Exception as e:
            print(e)
            response = self.wrap_json_response(code=1002, message="更新失败，请检查错误！")
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
            instance.if_deleted = True
            instance.save()
            response = self.wrap_json_response()

        except Exception as e:
            print(e)
            response = self.wrap_json_response(code=1002, message="删除资料失败，请检查错误！")

        return Response(response)

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)
        return Response({'errCode': 0, 'errMessage': '新增成功'})


