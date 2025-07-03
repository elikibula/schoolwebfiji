from django.urls import path
from . import views
from .views import login_view, dashboard_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_view, name='about'),
    path('students/', views.students_view, name='students'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    
]

 

