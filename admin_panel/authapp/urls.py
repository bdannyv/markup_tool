from django.urls import include, path

urlpatterns = [
    path('v1/', include('authapp.api.v1.urls'))
]
