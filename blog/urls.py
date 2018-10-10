from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/<slug:slug>_<int:pk>/', views.blog_detail, name='blog_detail'),
]
