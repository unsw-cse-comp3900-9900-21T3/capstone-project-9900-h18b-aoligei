from django.db import models
from django.contrib.auth.models import User


# Create your models here. 连接跟数据库的操作 class
# class User():
#     def __str__(self):
#         # Help humanized display object information
#         return self.username
#     class Meta:
#         verbose_name = 'user'
#         verbose_name_plural = "users"


class PersonalInfo(models.Model):

    firstname = models.CharField(max_length=200, null=False)
    lastname = models.CharField(max_length=200, null=False)
    gender = models.CharField(max_length=200, null=False)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    country = models.CharField(max_length=200, null=False)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE,db_column='user_id', null=False)

    def __str__(self):
        return self.code



class EmailVertifyCode(models.Model):
    code = models.CharField(max_length=20, verbose_name="email vertify")
    email = models.EmailField(max_length=200, verbose_name="vertify email")
    send_type = models.IntegerField(choices=((1, 'register'), (2, 'forget'), (3, 'change')),
                                    verbose_name="type of vertification")

    # add_time = models.DateTimeField(default=datetime.now,verbose_name="add time")
    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Email verification code information"
        verbose_name_plural = verbose_name
