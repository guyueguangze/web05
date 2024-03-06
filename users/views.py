import os.path
import re

from django.http import FileResponse
from rest_framework import status, viewsets, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

# Create your views here.
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView

from users.models import User, Addr, AddrSerializer
from users.permissions import UserPermissions
from users.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated

from web05.settings import MEDIA_ROOT


class LoginView(TokenObtainPairView):

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        # 自定义登录成功之后返回的结果
        result = serializer.validated_data
        result['mobile'] = serializer.user.mobile
        result['email'] = serializer.user.email
        result['username'] = serializer.user.username
        result['token'] = result.pop('access')
        result['id'] = serializer.user.id

        return Response(result, status=status.HTTP_200_OK)


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        password_confirmation = request.data.get('password_confirmation')
        if not all([username, password, email, password_confirmation]):
            return Response({'error': '用户所有参数不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': '用户名已存在'}, status=status.HTTP_400_BAD_REQUEST)
        if password != password_confirmation:
            return Response({'error', '两次密码不一致'}, status=status.HTTP_400_BAD_REQUEST)
        if not 6 <= len(password) <= 18:
            return Response({'error': '密码长度6-18位之间'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': '该邮箱已被注册'}, status=status.HTTP_400_BAD_REQUEST)

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return Response('邮箱格式不正确', status=status.HTTP_400_BAD_REQUEST)

        obj = User.objects.create_user(username=username, email=email, password=password)
        res = {
            'username': username,
            'email': obj.email,
            'id': obj.id
        }
        return Response(res, status=status.HTTP_201_CREATED)


class UserView(GenericViewSet, mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserPermissions]

    def upload_avatar(self, request, *args, **kwargs):
        avatar = request.data.get('avatar')
        if not avatar:
            return Response({'error': "上传失败文件不能为空"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # if avatar.size > 1024 * 300:
        #     return Response({'error': '文件大小不能超过300kb'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        user = self.get_object()
        ser = self.get_serializer(user, data={"avatar": avatar}, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({'url': ser.data['avatar']}, status=status.HTTP_200_OK)


class FileView(APIView):
    def get(self, request, name):
        path = MEDIA_ROOT / name
        if os.path.isfile(path):
            return FileResponse(open(path, 'rb'))
        return Response({'error': '没有找到该文件'}, status=status.HTTP_404_NOT_FOUND)
        # return Response({'code':"成功获取图片：{}".format(name)})


class AddrView(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
               mixins.UpdateModelMixin):
    queryset = Addr.objects.all()
    serializer_class = AddrSerializer
