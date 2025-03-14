

from django.contrib import admin
from django.urls import path
from app_book import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chapters/', views.heads, name='heads'),
    path('chapters/<int:pk>/', views.chapter, name='chapter'),
    path('', views.greeting, name='greeting'),
    path('postcards', views.postcards, name='postcards'),
    path('add_to_favorite/<int:id>', views.add_to_favorite, name='add_to_favorites'),
    path('favorites/', views.favorites, name='favorites')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

