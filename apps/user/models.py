from django.contrib.auth.models import AbstractUser
from django.db import models

class UserInfo(AbstractUser):
    """用户表"""
    username = models.CharField(max_length=32,verbose_name="用户名",unique=True)
    password = models.CharField(max_length=128,verbose_name="密码")
    mobile = models.CharField(max_length=11, verbose_name='手机号码', unique=True)
    score = models.IntegerField(default=0,verbose_name='用户得分')
    class Meta:
        db_table = "user"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name