from django.urls import path
from image_markup.api.v1 import views

urlpatterns = [
    path('statistics/', views.statistics_view, name='stat'),
    path('unlabeled/', views.get_unlabeled_image_id, name='unlabeled-image'),
    path('image/<uuid:id>', views.get_image, name='get-image'),
    path('labeled/', views.labeled_image, name='lebeled-message')
]
