from django.urls import path
from .views import (
                    payment_method_view,
                    payment_method_create_view
                )

app_name = "billing"

urlpatterns = [
    path('payment/', payment_method_view,name="payment"),
    path('payment/add-card/', payment_method_create_view,name="add-card"),

]
