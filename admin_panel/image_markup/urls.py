from django.urls import path
from image_markup import views

urlpatterns = [
    path('statistics/', views.my_view, name='stat'),
]
