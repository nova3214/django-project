from django.urls import path
from . import views  
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('history/', views.history, name='history'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('apply/', views.apply, name='apply'),
    path('applications/', views.application_list, name='application_list'),
    path('applications/<int:application_id>/approve/', views.approve_application, name='approve_application'),
    path('applications/<int:application_id>/reject/', views.reject_application, name='reject_application'),
    path('applications/', views.application_list, name='application_list'),  
    path('applications/<int:application_id>/approve/', views.approve_application, name='approve_application'),
    path('applications/<int:application_id>/reject/', views.reject_application, name='reject_application'),
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('application-status/', views.application_status, name='application_status'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
]

