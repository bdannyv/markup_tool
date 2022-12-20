from django.urls import path
from image_markup.api.v1 import views

urlpatterns = [
    path('statistics/', views.my_view, name='stat'),
]
