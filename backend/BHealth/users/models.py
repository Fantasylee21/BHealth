import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """用户模型类"""
    # 增加mobile字段
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    email = models.EmailField(verbose_name='邮箱', unique=True)
    avatar = models.ImageField(verbose_name='头像', blank=True, null=True, upload_to='avatar')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')
    introduction = models.TextField(verbose_name='个人简介', blank=True, null=True)
    # type = models.CharField(max_length=10, verbose_name='用户类型', default='normal')
    Types = (
        ('患者', '患者'),
        ('医生', '医生'),
        ('药库管理者', '药库管理者'),
    )
    type = models.CharField(max_length=20, choices=Types, default='患者')
    workSchedule = models.JSONField(verbose_name='工作时间表', blank=True, null=True)
    diagnosis = models.ManyToManyField('Diagnosis', related_name='diagnosis', blank=True)
    category = models.CharField(max_length=20, verbose_name='科室类别', default='normal')

    class Meta:
        db_table = 'users'
        verbose_name = '用户表'

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    # 验证码
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱", default="894618229@qq.com")
    # 包含注册验证和找回验证
    send_type = models.CharField(verbose_name="验证码类型", max_length=10,
                                 choices=(("register", "注册"), ("forget", "找回密码")))
    send_time = models.DateTimeField(verbose_name="发送时间", default=datetime.datetime.now())

    class Meta:
        verbose_name = u"2. 邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)


class Diagnosis(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='医生')
    content = models.TextField(verbose_name='诊断内容')
    is_taken = models.BooleanField(default=False, verbose_name='是否已取药')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'diagnosis'
        verbose_name = '诊断表'

    def __str__(self):
        return self.content
