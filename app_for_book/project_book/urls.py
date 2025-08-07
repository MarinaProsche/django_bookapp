from django.contrib import admin
from django.urls import path, re_path, include
from app_book import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from pwa import views as pwa_views

urlpatterns = [
    # path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('admin/', admin.site.urls),
    path('chapters/', views.heads, name='heads'),
    path('chapters/<int:pk>/', views.chapter, name='chapter'),
    path('', views.greeting, name='greeting'),
    path('postcards', views.postcards, name='postcards'),
    path('add_to_favorite/<int:pic_id>/', views.add_to_favorite, name='add_to_favorites'),
    path('favorites/', views.favorites, name='favorites'),
    path('logout/', views.logout_view, name='logout'),
    path('map/', views.map, name='map'),
    path('postcard/<int:target_buzzword>/', views.single_postcard, name='single_postcard'),
    path('registration/', views.registration, name='registration'),
    path('instruction/', views.instruction, name='instruction'),
    path('', include('pwa.urls')),
    # path('how_to_read/', views.how_to_read, name='read'),


    re_path(r'^manifest\.json$', pwa_views.manifest, name='manifest'),
    re_path(r'^serviceworker\.js$', pwa_views.service_worker, name='serviceworker'),
    path('offline/', pwa_views.offline, name='offline'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
