from django.urls import path
from . import views


app_name = "accounts"
urlpatterns = [
    path('mypage/', views.mypage, name='mypage'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('password/', views.change_password, name='change_password'),
]
