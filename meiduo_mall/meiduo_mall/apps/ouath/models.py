from django.db import models

# Create your models here.
from meiduo_mall.utils.models import BaseModel


class OAuthQQUser(BaseModel):
    '''关系映射表'''
    #用户表drf自带
    #默认是另一张表的主键关联
    user = models.ForeignKey('users.User',verbose_name='用户')
    openid = models.CharField(max_length=64, verbose_name='openid', db_index=True)

    class Meta:
        db_table = 'tb_oauth_qq'
        verbose_name = 'QQ登录用户数据'
        verbose_name_plural = verbose_name