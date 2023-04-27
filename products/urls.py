from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('products/<int:product_pk>/comments/create/', views.comments_create, name='comments_create'),
]
