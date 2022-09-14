from django.urls import path
from accounts import views as AccountViews
from .  import views

urlpatterns = [
    path('admindashboard/', AccountViews.adminDashboard, name='admindashboard'),
    path('vendors/', views.vendors, name='adminvendor'),
    path('vendors/<slug:vendor_slug>/', views.vendor_detail, name='vendor_detail'),
    path('orders/', views.admin_orders_detail, name='admin_orders_detail'),
    
    path('<slug:vendor_slug>/orders/', views.admin_vendor_order_detail, name='admin_vendor_order_detail'),
    path('order_detail/<int:order_number>', views.admin_customer_order_detail, name='admin_customer_order_detail'),

    path('customers/', views.customers, name='admin_customers'),
    

]