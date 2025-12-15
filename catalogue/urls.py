
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home' ),
    path('contact/', views.contact , name='contact' ),
    path('detail/<int:pk>/', views.detail , name='detail' ),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('offered-rates/', views.offered_rates, name='offered_rates')
]