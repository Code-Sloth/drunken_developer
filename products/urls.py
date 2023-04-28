from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('products/<int:product_pk>/comments/create/', views.comment_create, name='comment_create'),
    path('products/<int:product_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('products/<int:product_pk>/likes/', views.likes, name='likes'),
    path('products/<int:product_pk>/delete/', views.delete, name='delete'),
    path('products/<str:category>/', views.listing, name='listing'),
]