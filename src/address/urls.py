from django.urls import path
from .views import (
            checkout_address_create_view,
            checkout_address_reuse_view
        )

app_name = "address"

urlpatterns = [
    path('', checkout_address_create_view,name="addresses"),
    path('select-address/', checkout_address_reuse_view,name="address_reuse"),
    
]
