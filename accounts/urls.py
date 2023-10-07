from django.urls import path
from . import views


urlpatterns = [
    path('register-user/', views.register_user, name='registerUser'),
    path('register-vendor/', views.register_vendor, name='registerVendor'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('my-account/', views.my_account, name='myAccount'),
    path('customer-dashboard/', views.customer_dashboard, name='customerDashboard'),
    path('vendor-dashboard/', views.vendor_dashboard, name='vendorDashboard'),
]

