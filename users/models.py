from django.db import models
from rest_framework import serializers

from common.db import BaseModel
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    mobile = models.CharField(verbose_name='手机号', default='', max_length=11)
    avatar = models.ImageField(verbose_name='用户头像', blank=True, null=True)

    class Meta:
        db_table = 'users'
        verbose_name = '用户表'


class Addr(models.Model):
    user = models.ForeignKey('User', verbose_name='所属用', on_delete=models.CASCADE)
    phone = models.CharField(verbose_name='手机号码', max_length=11, default='')
    name = models.CharField(verbose_name='联系人', max_length=20)
    province = models.CharField(verbose_name='省份', max_length=20)
    city = models.CharField(verbose_name='城市', max_length=20)
    county = models.CharField(verbose_name='区县', max_length=20)
    address = models.CharField(verbose_name='详细地址', max_length=100)
    is_default = models.BooleanField(verbose_name='是否为默认地址', default=False)

    class Meta:
        db_table = 'addr'
        verbose_name = '收货地址表'


class Area(models.Model):
    pid = models.IntegerField(verbose_name='上级id', default=0)
    name = models.CharField(verbose_name='地区名', max_length=20)
    level = models.IntegerField(verbose_name='区域等级', default=0)

    class Meta:
        db_table = 'area'
        verbose_name = '地区表'


class VerifCode(models.Model):
    mobile = models.CharField(verbose_name='手机号码', max_length=11)
    code = models.CharField(verbose_name='验证码', max_length=6)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='生成时间')

    class Meta:
        db_table = 'verif_code'
        verbose_name = '验证码'


class AddrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addr
        fields = '__all__'
