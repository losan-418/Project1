from django.db import models

class UserModel(models.Model):
    uid=models.IntegerField()
    uname=models.CharField(max_length=50)
    upass=models.CharField(max_length=15)
    uemail=models.EmailField()
    usname=models.CharField(max_length=100)
    def __str__(self):
        return self.name
# Create your models here.
