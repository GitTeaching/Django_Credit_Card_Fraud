from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict', views.predict_view, name='predict_view'),
    path('predict_using_api', views.predict_using_api, name='predict_using_api'),
    path('notebook', views.notebook, name='notebook'),
]