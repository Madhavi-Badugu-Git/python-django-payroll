from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('payslip/<int:pk>/', views.payslip, name='payslip'),
    
    # Remaining URLs mapped from your templates folder:
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
]