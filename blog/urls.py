from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:slug>', views.search, name='search'),
    path('<slug:cat_slug>/<slug:slug>-<int:pk>/', views.blog_detail, name='blog_detail'),
]
