from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('admin-view/', views.admin_view, name='admin_view'),
    path('add_product/', views.add_product, name='add_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('category_product/<int:category_id>/', views.category_products, name='category_products'),
    path('product_detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('about/', views.about, name='about'),
    path('all_products/', views.all_products, name='all_products'),
    path('sales/', views.sales, name='sales'),
    path('category_summary/', views.category_summary, name='category_summary'),
]