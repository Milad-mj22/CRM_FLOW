from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Mine(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام معدن')
    city = models.CharField(max_length=100)
    location = models.CharField(max_length=300, verbose_name='موقعیت جغرافیایی')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='ایجادکننده')

    def __str__(self):
        return self.name
