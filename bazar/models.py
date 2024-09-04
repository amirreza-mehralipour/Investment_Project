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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    initial_amount = models.FloatField()
    start_month = models.CharField(max_length=20, choices=MONTH_CHOICES)
    end_month = models.CharField(max_length=20, choices=MONTH_CHOICES)
    assets = models.ManyToManyField(Asset, related_name='sandoghs')

    def __str__(self) -> str:
        return f"{self.user.username}'s Sandogh"


class ProfitCalculationHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calculation_date = models.DateTimeField(auto_now_add=True)
    initial_amount = models.FloatField()
    start_month = models.CharField(max_length=20)
    end_month = models.CharField(max_length=20)
    results = models.JSONField()

    def __str__(self):
        return f'{self.user.username} - {self.calculation_date}'