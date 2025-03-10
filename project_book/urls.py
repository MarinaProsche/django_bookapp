

from django.contrib import admin
from django.urls import path
from app_book import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chapters/', views.heads, name='heads'),
    path('chapters/<int:pk>/', views.chapter, name='chapter'),
    path('', views.greeting, name='greeting'),
]
