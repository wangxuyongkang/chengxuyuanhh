from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from bokeapp.models import Token,User


class MyBaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request._request.GET.get('token')
        obj = Token.objects.filter(token=token).first()
        if obj:
            # 用户登录了
            # user auth
            return (obj.user, token)
        else:
            raise AuthenticationFailed('用户未登录')
