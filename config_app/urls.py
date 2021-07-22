from django.urls import path
from .views import CheckConfigAPIView, ConfigAPIView, ListConfigAPIView, TemplateAPIView

urlpatterns = [
    path('config/create', ConfigAPIView.as_view()),
    path('template', TemplateAPIView.as_view()),
    path('config', ListConfigAPIView.as_view()),
    path('config/check', CheckConfigAPIView.as_view())
]

