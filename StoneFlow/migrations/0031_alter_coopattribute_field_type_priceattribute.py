# Generated by Django 5.1.1 on 2025-07-13 18:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StoneFlow', '0030_cuttingaround'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coopattribute',
            name='field_type',
            field=models.CharField(choices=[('int', 'عدد صحیح'), ('float', 'عدد اعشاری'), ('str', 'متن'), ('select', 'منوی کشویی'), ('bool', 'چک\u200cباکس'), ('image', 'تصویر'), ('material', 'ماده اولیه'), ('warehouse', 'انبار'), ('Cutting_factory', 'کارخانه برش اره'), ('CuttingSaw', 'موارد برش اره'), ('CuttingAround', 'موارد دور بور شده'), ('multi_select', 'چک\u200cباکس چندتایی'), ('date', 'تاریخ (شمسی)'), ('price', 'قیمت')], max_length=20),
        ),
        migrations.CreateModel(
            name='PriceAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('multiplier', models.DecimalField(decimal_places=2, default=1.0, max_digits=10, verbose_name='ضریب')),
                ('attribute', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='price_attr', to='StoneFlow.coopattribute')),
            ],
        ),
    ]
