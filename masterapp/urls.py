from django.urls import path
from .views import home, register_worker

urlpatterns = [
    path('', home, name = 'home'),
    path('worker', register_worker, name = 'register_worker')
]
