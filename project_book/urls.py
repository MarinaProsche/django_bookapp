from django.contrib import admin
from django.urls import path, include
from app_book import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page
from pwa import views as pwa_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chapters/', views.heads, name='heads'),
    path('chapters/<int:pk>/', views.chapter, name='chapter'),
    path('', views.greeting, name='greeting'),
    path('postcards', views.postcards, name='postcards'),
    path('add_to_favorite/<int:pic_id>/', views.add_to_favorite, name='add_to_favorites'),
    path('favorites/', views.favorites, name='favorites'),
    path('logout/', views.logout_view, name='logout'),
    path('map/', views.map, name='map'),
    path('', include('pwa.urls')),
    # path('offline/', cache_page(settings.PWA_APP_NAME)(pwa_views.offline.as_view())),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

