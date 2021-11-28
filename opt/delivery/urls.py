from django.urls import path

from . import views

urlpatterns = [
    path('recruit/', views.register_bus),
    path('show/', views.obtain_carriable_bus),
    path('reserve/', views.reserve_bus),
    path('accept/', views.check_accept),
    path('finish/', views.check_finish),
]
