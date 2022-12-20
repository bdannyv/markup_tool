from authapp.api.v1 import views
from django.urls import path

urlpatterns = [
    path('signup', views.signup, name='custom-signup'),
    path('signin', views.signin, name='custom-signin'),
]
