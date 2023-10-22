from django.urls import path
from . import views
from accounts import views as AccountViews


urlpatterns = [
    path('', AccountViews.vendor_dashboard, name='vendor'),
    path('profile/', views.vendor_profile, name='vendorProfile'),
    path('menu-builder/', views.menu_builder, name='menuBuilder'),
    path('menu-builder/category/<int:pk>/', views.fooditems_by_category, name='fooditemsByCategory'),

    # Category CRUD
    path('menu-builder/category/create/', views.add_category, name='addCategory'),
    path('menu-builder/category/update/<int:pk>/', views.edit_category, name='editCategory'),
    path('menu-builder/category/delete/<int:pk>/', views.delete_category, name='deleteCategory'),
]
