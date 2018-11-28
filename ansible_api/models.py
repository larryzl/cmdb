from django.db import models
import uuid
from users.models import CustomUser
# Create your models here.

class AnsibleServerGroup(models.Model):
    name = models.CharField(max_length=30,unique=True)
    describe = models.CharField(max_length=50,blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ansible主机组"
        verbose_name_plural = "ansible主机组"



