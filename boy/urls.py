from django.urls import path
from .views import GreetView


urlpatterns = [
    path('api/hello', GreetView.as_view(), name='hello'),
]
