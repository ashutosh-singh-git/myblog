from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/', views.search, name='category'),
    path('category/<slug:slug>', views.search, name='search'),
    path('<slug:cat_slug>/<slug:slug>-<int:pk>/', views.blog_detail, name='blog_detail'),
]
