from django.urls import path
from .views import HomeApiView, ResultApiView



urlpatterns = [
    path('', HomeApiView.as_view(), name='home'),
    path('result', ResultApiView.as_view(), name='result'),
]
