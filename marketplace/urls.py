from django.urls import path,include

from . import views

urlpatterns = [
    # ADD TO CART
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    # DECREASE CART
    path('decrease_cart/<int:product_id>/', views.decrease_cart, name='decrease_cart'),
    # DELETE CART ITEM
    path('delete_cart/<int:cart_id>/', views.delete_cart, name='delete_cart'),

]