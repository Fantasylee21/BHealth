from django.db import models


# Create your models here.

class Drug(models.Model):
    """药品模型类"""
    name = models.CharField(max_length=20, verbose_name='药品名称',unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    stock = models.IntegerField(default=1, verbose_name='库存')
    description = models.TextField(verbose_name='药品描述')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除  ')

    class Meta:
        db_table = 'drugs'
        verbose_name = '药品表'

    def __str__(self):
        return self.name
