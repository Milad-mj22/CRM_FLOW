from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# models.py
class Task(models.Model):
    from users.models import Buyer

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(verbose_name="تاریخ پیگیری",null=True,blank=True)
    created_date = models.DateField(verbose_name="تاریخ ایجاد",auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True,related_name='task_sasign_to')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='task_created_by')
    is_active = models.BooleanField(default=True) 
    is_done = models.BooleanField(default=False) 

    

    buyer = models.ForeignKey(
        Buyer,
        on_delete=models.CASCADE,
        related_name='task_buyer',
        verbose_name="خریدار ",
        null = True,
        blank = True
    )
    


    
    def __str__(self):
        return self.title
    


class CommentTask(models.Model):

    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_coment')  # محصولی که تولید شده
    description = models.TextField(blank=True)
    created_date = models.DateField(verbose_name="تاریخ ایجاد",auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True,related_name='comment_task_assign_to')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comment_task_assign_by')
     