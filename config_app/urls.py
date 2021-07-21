from django.urls import path
from .views import ConfigAPIView, TemplateAPIView

urlpatterns = [
    path('config/create', ConfigAPIView.as_view()),
    path('template', TemplateAPIView.as_view())
]
