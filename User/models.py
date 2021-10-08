from django.db import models

# Create your models here. 连接跟数据库的操作 class
class User():
    def __str__(self):
        # Help humanized display object information
        return self.username

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = "users"

