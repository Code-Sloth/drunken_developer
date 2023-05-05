from django.urls import path
from . import views


app_name = 'products'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:product_pk>/pay_success/', views.pay_success, name='pay_success'),
    path('pay_fail/', views.pay_fail, name='pay_fail'),
    path('pay_cancel/', views.pay_cancel, name='pay_cancel'),
    path('<int:product_pk>/', views.detail, name='detail'),
    path('<int:product_pk>/delete/', views.delete, name='delete'),
    path('<int:product_pk>/update/', views.update, name='update'),
    path('<int:product_pk>/comments/', views.comment_create, name='comment_create'),
    path('<int:product_pk>/comments/<int:comment_pk>/update/', views.comment_update, name='comment_update'),
    path('<int:product_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:product_pk>/likes/', views.likes, name='likes'),
    path('<int:product_pk>/delete/', views.delete, name='delete'),
    path('<int:product_pk>/kakaopay/', views.kakaopay, name='kakaopay'),
    path('listing/', views.listing, name='listing'),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz_response/', views.quiz_response, name='quiz_response'),
    path('new_chat/', views.new_chat, name='new_chat'),
]
