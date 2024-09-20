import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class WorkSchedule(models.Model):
    from_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    num = models.IntegerField(verbose_name='剩余数量')
    doctor = models.ForeignKey('User', on_delete=models.CASCADE, related_name='doctor')



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
        ('patient', 'patient'),
        ('doctor', 'doctor'),
        ('pharmacist', 'pharmacist'),
    )
    type = models.CharField(max_length=20, choices=Types, default='patient')
    category = models.CharField(max_length=20, verbose_name='科室类别', default='normal')

    class Meta:
        db_table = 'users'
        verbose_name = '用户表'

    def __str__(self):
        return self.username


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Doctor')
    content = models.TextField(verbose_name='预约内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    time = models.DateTimeField(verbose_name='预约时间')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'appointment'
        verbose_name = '预约表'

    def __str__(self):
        return self.content


class EmailVerifyRecord(models.Model):
    # 验证码
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    # 包含注册验证和找回验证
    send_type = models.CharField(verbose_name="验证码类型", max_length=10)
    send_time = models.DateTimeField(auto_now=True, verbose_name="发送时间")

    class Meta:
        db_table = "email_verify"
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name


class Diagnosis(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='医生')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='患者')
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
