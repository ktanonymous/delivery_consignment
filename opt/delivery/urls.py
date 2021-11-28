from django.urls import path

from . import views

urlpatterns = [
    path('recruit/', views.register_bus),
    path('show/', views.obtain_carriable_bus),
    path('reserve/', views.reserve_bus),
    path('time_table/', views.set_time_table),
]
