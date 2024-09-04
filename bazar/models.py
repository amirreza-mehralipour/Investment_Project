from django.db import models
from django.contrib.auth.models import User

class Asset(models.Model):
    name = models.CharField(max_length=100)
    monthly_prices = models.JSONField()

    def __str__(self):
        return self.name

class Sandogh(models.Model):
    MONTH_CHOICES = [
        ('Farvardin', 'Farvardin'),
        ('Ordibehesht', 'Ordibehesht'),
        ('Khordad', 'Khordad'),
        ('Tir', 'Tir'),
        ('Mordad', 'Mordad'),
        ('Shahrivar', 'Shahrivar'),
        ('Mehr', 'Mehr'),
        ('Aban', 'Aban'),
        ('Azar', 'Azar'),
        ('Dey', 'Dey'),
        ('Bahman', 'Bahman'),
        ('Esfand', 'Esfand'),
    ]
    initial_amount = models.FloatField()
    start_month = models.CharField(max_length=20, choices=MONTH_CHOICES)
    end_month = models.CharField(max_length=20, choices=MONTH_CHOICES)
    assets = models.ManyToManyField(Asset, related_name='sandoghs')

