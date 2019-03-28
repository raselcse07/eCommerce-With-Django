from django.urls import path
from  .views import (
                    cart_home,
                    cart_update,
                    checkout_home,
                    checkout_done,
                    cart_update_api_view
                )

app_name = "cart"

urlpatterns = [
    path('', cart_home,name="cart-home"),
    path('update/', cart_update,name="cart-update"),
    path('checkout/', checkout_home,name="checkout"),
    path('checkout/success/', checkout_done,name="checkout-success"),
    path('api/', cart_update_api_view,name="cart-update-api"),
]
