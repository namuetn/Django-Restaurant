from django.urls import path
from . import views


urlpatterns = [
    path('register-user/', views.register_user, name='registerUser')
]

