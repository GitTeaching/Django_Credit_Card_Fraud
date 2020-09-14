from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_overview, name='api_overview'),
    path('get_preds_api/', views.get_preds_api, name='get_preds_api'),
    path('get_preds_api_columns/', views.get_preds_api_columns, name='get_preds_api_columns'),
]