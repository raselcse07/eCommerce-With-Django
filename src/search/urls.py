from django.urls import path
from .views import (
                SearchProductView
            )

app_name = "search"

urlpatterns = [

    # product list
    path('', SearchProductView.as_view(),name="product-search"),

]
