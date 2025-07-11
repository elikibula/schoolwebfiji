from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.document_list, name='document_list'),
    path('upload/', views.upload_document, name='upload_document'),
    path('downloads/', views.download_view, name='downloads'),
    path('downloads/subcategory/<int:pk>/', views.download_subcategory_detail, name='download_subcategory_detail'),

    # Use primary key instead of slug
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('subcategory/<int:pk>/', views.subcategory_detail, name='subcategory_detail'),

    path('get-subcategories/', views.get_subcategories, name='get_subcategories'),

    # Document views now use pk
    path('document/<int:pk>/', views.document_detail, name='document_detail'),
    path('document/<int:pk>/download/', views.download_document, name='download_document'),
    path('document/<int:pk>/view/', views.view_document, name='view_document'),
    path('document/<int:pk>/edit/', views.update_document, name='update_document'),
    path('document/<int:pk>/delete/', views.delete_document, name='delete_document'),
    path('preview/<int:pk>/', views.embedded_preview, name='embedded_preview'),
    
]
