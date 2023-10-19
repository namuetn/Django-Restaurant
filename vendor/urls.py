from django.urls import path, include
from . import views
from accounts import views as AccountViews


urlpatterns = [
    path('', AccountViews.vendor_dashboard, name='vendor'),
    path('profile/', views.vendor_profile, name='vendorProfile'),
]
