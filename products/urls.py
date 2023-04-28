from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:product_pk>/', views.detail, name='detail'),
    path('<int:product_pk>/delete/', views.delete, name='delete'),
    path('<int:product_pk>/update/', views.update, name='update'),
    path('<int:product_pk>/comments/create/', views.comment_create, name='comment_create'),
    path('<int:product_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:product_pk>/likes/', views.likes, name='likes'),
    path('<int:product_pk>/delete/', views.delete, name='delete'),
    path('listing/', views.listing, name='listing'),
]
