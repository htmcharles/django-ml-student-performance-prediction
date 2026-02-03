from django.urls import path
from .views import predict_performance, predict_ui

urlpatterns = [
    path('predict/', predict_performance),
    path('', predict_ui, name='predict_ui'),
]
