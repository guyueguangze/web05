from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import serializers

from users.models import User


class MyBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username) | Q(mobile=username))
        except:
            return serializers.ValidationError({'error': '未找到该用户'})
        else:
            if user.check_password(password):
                return user
            else:
                return serializers.ValidationError({'error': '密码错误'})
