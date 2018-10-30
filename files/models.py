from django.db import models
from users.models import CustomUser
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Files(models.Model):

    user = models.ForeignKey(CustomUser,verbose_name="用户名",related_name="users",on_delete=models.CASCADE)
    file_name = models.FileField(upload_to="upload/%Y%m%d")
    description = models.TextField(verbose_name=u"介绍", blank=True, null=True, )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    def __unicode__(self):
        return self.user


