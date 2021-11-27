from django.urls import path

from . import views

urlpatterns = [
    path('recruit/', views.register_bus),
]