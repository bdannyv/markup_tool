from django.urls import include, path

urlpatterns = [
    path('v1/', include('image_markup.api.v1.urls')),
]
