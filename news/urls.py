from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('create/', views.create_news, name='create_news'),
    path('<slug:slug>/edit/', views.update_news, name='update_news'),
    path('<slug:slug>/delete/', views.delete_news, name='delete_news'),
    path('<slug:slug>/', views.news_detail, name='news_detail'),
    path('category/<slug:slug>/', views.category_view, name='category_view')
]
