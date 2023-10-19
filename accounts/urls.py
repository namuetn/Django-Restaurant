from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.my_account),
    path('register-user/', views.register_user, name='registerUser'),
    path('register-vendor/', views.register_vendor, name='registerVendor'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('my-account/', views.my_account, name='myAccount'),
    path('customer-dashboard/', views.customer_dashboard, name='customerDashboard'),
    path('vendor-dashboard/', views.vendor_dashboard, name='vendorDashboard'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('forgot-password/', views.forgot_password, name='forgotPassword'), 
    path('reset-password-validate/<uidb64>/<token>/', views.reset_password_validate, name='resetPasswordValidate'), 
    path('reset-password/', views.reset_password, name='resetPassword'),

    path('vendor/', include('vendor.urls'))
]
