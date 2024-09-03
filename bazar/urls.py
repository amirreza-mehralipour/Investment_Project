from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('calculate_profit/', views.CalculateProfitView.as_view(), name='calculate_profit'),
    path('find_best_investment_period/<str:name>/', views.find_best_investment_period, name='find_best_investment_period'),
    path('login/', Login.as_view()),
    path('refresh/', Refresh.as_view()),
]