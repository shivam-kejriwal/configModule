from django.urls import path
from .views import *

urlpatterns = [
    path('config/create', ConfigAPIView.as_view()),
    path('template', TemplateAPIView.as_view()),
    path('config', ListConfigAPIView.as_view()),
    path('config/check', CheckConfigAPIView.as_view()),
    path('config/bulkUpdate', BulkUpdateAPIView.as_view()),
    path('config/<uuid:config_id>', EditConfigAPIView.as_view()),
]

