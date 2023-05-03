from django.urls import path
from . import views


app_name = "accounts"
urlpatterns = [
    path('mypage/<str:username>/', views.mypage, name='mypage'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('password/', views.change_password, name='change_password'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
    path('<str:username>/like/', views.like, name='like'),
    path('<str:username>/review/', views.review, name='review'),
    path('<str:username>/profile/', views.profile, name='profile'),
    path('<str:username>/purchase/', views.purchase, name='purchase'),
]
