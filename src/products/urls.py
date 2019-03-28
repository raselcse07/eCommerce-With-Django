from django.urls import path
from .views import (
                ProductList,
                ProductDetail,
                FeaturedProductListView,
                CategoryDetail
            )

app_name = "products"

urlpatterns = [

    # product list
    path('list/', ProductList.as_view(),name="product-list"),
    # featured product list
    path('featured/list/', FeaturedProductListView.as_view(),name="featured-product-list"),
    # product detail
    path('<slug:slug>/detail/', ProductDetail.as_view(),name="product-detail"),
    path('category/<slug:slug>/detail/', CategoryDetail.as_view(),name="category-detail"),
]
