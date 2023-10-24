from django.urls import path

from marketplace import views

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('<slug:vendor_slug>/', views.vendor_detail, name='vendorDetail'),

    # Add to cart
    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='addToCart'),
    path('decrease-cart/<int:food_id>/', views.decrease_cart, name='decreaseCart'),
]
