from django.shortcuts import render
from rest_framework.views import APIView
from bokeapp.serializers import UserSerializers,CategorySerializers,BokeListSerializers,BokedetailSeralizers,CommentSeralizers
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin,ListModelMixin
from rest_framework.response import Response
from rest_framework import status
from bokeapp.models import User, Token,Category,Boke,comments
from bokeapp.utils.pagination import MyPageNumberPagination
from bokeapp.utils.authenandpermission import MyBaseAuthentication
# Create your views here.

import time
import hashlib

def get_token(username, password):
    # 根据用户名， 密码， time_str 生成token
    time_str = str(int(time.time() * 1000))
    md5_obj = hashlib.md5(time_str.encode('utf8'))
    md5_obj.update(username.encode('utf8'))
    md5_obj.update(password.encode('utf8'))
    return md5_obj.hexdigest()


class RegisterView(GenericViewSet, CreateModelMixin):
    serializer_class = UserSerializers

    def create(self, request, *args, **kwargs):
        ret = {
            'code': 1,
            'msg': '注册成功'
        }
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(ret, status=status.HTTP_201_CREATED, headers=headers)
        else:
            msgs = serializer.errors
            ret['code'] = 0
            ret['msg'] = msgs
            return Response(ret)


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        ret = {
            'code': 1,
            'msg': '登陆成功'
        }
        try:
            # 获取post请求数据
            data = request.data
            # 获取user
            name = data.get('name')
            password = data.get('password')
            obj = User.objects.filter(name=name).first()
            print(obj)
            if obj:
                # 存在
                if obj.password == password:
                    token = get_token(name, password)
                    Token.objects.update_or_create(user=obj, defaults={'token': token})
                    ret['token'] = token
                else:
                    ret['code'] = 0
                    ret['msg'] = '密码错误,请重试'
            else:
                ret['code'] = 0
                ret['msg'] = '用户不存在'
        except Exception as err:
            print(err)
            ret['code'] = 0
            ret['msg'] = '异常错误,请重试!'
        return Response(ret)

class CategaryView(GenericViewSet,ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

class BokelistView(GenericViewSet,ListModelMixin):
    queryset = Boke.objects.all()
    serializer_class = BokeListSerializers
    # pagination_class = MyPageNumberPagination
    def list(self, request, *args, **kwargs):
        category_id = kwargs.get('pk')
        if category_id:
            books = Boke.objects.filter(category=category_id)
            serializer = self.get_serializer(books, many=True)
            return Response(serializer.data)

class BokelistallView(GenericViewSet,ListModelMixin):
    queryset = Boke.objects.all()
    serializer_class = BokeListSerializers
    pagination_class = MyPageNumberPagination
    def list(self, request, *args, **kwargs):
        ret = {
            'code':1
        }
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(ret,serializer.data)

class BokedetailView(GenericViewSet,ListModelMixin):
    queryset = Boke.objects.all()
    serializer_class = BokedetailSeralizers
    pagination_class = MyPageNumberPagination
    def list(self, request, *args, **kwargs):
        category_id = kwargs.get('pk')
        if category_id:
            books = Boke.objects.filter(category=category_id)
            serializer = self.get_serializer(books, many=True)
            return Response(serializer.data)

class CommentsView(GenericViewSet,CreateModelMixin):
    authentication_classes = [MyBaseAuthentication]
    queryset = comments.objects.all()
    serializer_class = CommentSeralizers
    def create(self, request, *args, **kwargs):
        ret = {
            'code': 1,
            'msg': '发表评论成功'
        }
        # get_serializer返回序列化对象
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(ret, status=status.HTTP_201_CREATED, headers=headers)
        else:
            print(serializer.errors)
            ret['code'] = 0
            ret['msg'] = '发表评论失败'
            return Response(ret)

#评论列表
class CommentlistsView(GenericViewSet,ListModelMixin):
    queryset = comments.objects.all()
    serializer_class = CommentSeralizers
    def list(self, request, *args, **kwargs):
        comment_id = kwargs.get('pk')
        if comment_id:
            comment = comments.objects.filter(id=comment_id)
            serializer = self.get_serializer(comment, many=True)
            return Response(serializer.data)
