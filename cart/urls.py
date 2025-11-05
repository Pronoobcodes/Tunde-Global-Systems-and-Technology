from django.urls import path
from . import views

urlpatterns = [
    path('cart_summary/', views.cart_summary, name='cart_summary'),
    path('add/' ,views.cart_add, name='cart_add'),
    path('delete/', views.cart_delete, name='cart_delete'),
    path('clear/', views.clear, name='cart_clear'),
    path('update/', views.cart_update, name='cart_update'),
    path('count/', views.cart_count, name='cart_count'),
]
