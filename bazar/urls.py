from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('calculate_profit/', views.CalculateProfitView.as_view(), name='calculate_profit'),
    path('find_best_investment_period/<str:name>/', views.FindBestInvestmentPeriodView.as_view()),
    path('login/', Login.as_view()),
    path('refresh/', Refresh.as_view()),
    path('asset/', ListCreateAsset.as_view()),
    path('sandogh/', CalculateProfitView.as_view()),]