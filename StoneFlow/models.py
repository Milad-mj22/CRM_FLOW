from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from users.models import raw_material
# Create your models here.

STATE_CHOICES = [
        ('transport', 'حمل و نقل'),
        ('warehouse', 'انبار کوپ'),
        ('accounting', 'حسابداری'),
        ('warehouse production', 'انبار تولید'),
        ('production', 'تولید'),
        ('factory_stock', 'افزودن به انبار کارخانه'),
        ('customer_order', 'سفارش مشتری'),
        ('showroom', 'نمایشگاه'),
]



class CoopStateHistory(models.Model):
    coop = models.ForeignKey('coops', on_delete=models.CASCADE, related_name='state_history')
    previous_state = models.CharField(max_length=30, choices=STATE_CHOICES)
    new_state = models.CharField(max_length=30, choices=STATE_CHOICES)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    changed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.coop.id} | {self.get_previous_state_display()} ➝ {self.get_new_state_display()} @ {self.changed_at}"
    


class coops(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='raw_material_submissions')
    material = models.ForeignKey(raw_material, on_delete=models.CASCADE, related_name='submissions')
    
    quantity = models.FloatField()
    submitted_at  = models.DateTimeField(default=timezone.now, null=True, blank=True)
    state = models.CharField(max_length=30, choices=STATE_CHOICES, default='transport')

    image = models.ImageField(upload_to='mining_remittance/', blank=True, null=True)  # Added field for image


    # فقط برای نگهداری موقتی کاربر تغییر دهنده
    _changed_by = None

    def __str__(self):
        return f"{self.user.username} - {self.material.name} - {self.get_state_display()}"

    def set_changed_by(self, user):
        self._changed_by = user

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        previous_state = None

        if not is_new:
            previous = coops.objects.get(pk=self.pk)
            previous_state = previous.state

        super().save(*args, **kwargs)  # اول ذخیره کن تا مطمئن باشیم pk داریم

        # فقط وقتی کوپ جدید هست و state = transport یا state تغییر کرده، لاگ بساز
        if (is_new and self.state == 'transport') or (not is_new and previous_state != self.state):
            CoopStateHistory.objects.create(
                coop=self,
                previous_state=previous_state if previous_state else 'New',
                new_state=self.state,
                changed_by=self._changed_by
            )




# models.py
from django.db import models
from django.contrib.auth.models import User

class CarModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    national_code = models.CharField(max_length=10, unique=True)
    car_model = models.ForeignKey(CarModel, on_delete=models.SET_NULL, null=True)
    license_plate = models.CharField(max_length=20)
    car_code = models.CharField(max_length=20)

    def __str__(self):
        return self.full_name
