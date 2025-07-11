from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static  # Import static
from django.contrib.auth import views as auth_views
from dashboard import views as dashboard_views


urlpatterns = [
    path('katubalevu/', admin.site.urls),
    path('', include('home.urls')),
    path('news/', include('news.urls')),
    path('documents/', include(('documents.urls', 'documents'), namespace='documents')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('tinymce/', include('tinymce.urls')),
    path('events/', include('events.urls')),
    path('dashboard/', include('dashboard.urls')),


   
]

# Serve media files only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    

