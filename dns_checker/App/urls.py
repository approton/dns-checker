from django.urls import path
from .views import check_dns_and_ssl

urlpatterns = [
    path('', check_dns_and_ssl, name='index'),
]
