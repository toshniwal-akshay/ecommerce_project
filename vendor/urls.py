from django.urls import path, include
from . import views
from accounts import views as AccountViews


urlpatterns = [
    path('', AccountViews.vendorDashboard, name='vendor'),
    path('profile/', views.vprofile, name='vprofile'),
    path('product-builder/',views.product_builder,name='productbuilder'),
    path('product-builder/category/<int:pk>/', views.products_by_category, name='productitems_by_category'),

    # Category CRUD
    path('product-builder/category/add/', views.add_category, name='add_category'),
    path('product-builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('product-builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),
    
     # Product CRUD
    path('product-builder/product/add/', views.add_product, name='add_product'),
    path('product-builder/product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('product-builder/product/delete/<int:pk>/', views.delete_product, name='delete_product'),
    
    path('order_detail/<int:order_number>/', views.order_detail, name='vendor_order_detail'),
    path('my_orders/', views.my_orders, name='vendor_my_orders'),
    
]