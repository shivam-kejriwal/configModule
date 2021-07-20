from django.urls import path
from .views import ConfigAPIView

urlpatterns = [
    path('config/create' , ConfigAPIView.as_view()),
]