from django.db import models


class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    front_image = models.ImageField(verbose_name='新闻封面', blank=True, null=True, upload_to='front_image')

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    discretion = models.TextField()

    class Meta:
        db_table = 'news'
        verbose_name = '新闻表'

    def __str__(self):
        return self.title
# Create your models here.
