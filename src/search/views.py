from django.shortcuts import render
from django.views.generic.list import ListView
from cart.models import Cart
from products.models import (
                    Product,
                    ProductCategory
                )



class SearchProductView(ListView):
    template_name = "products/product-list.html"

    def get_context_data(self,*args,**kwargs):
        request = self.request
        context = super(SearchProductView,self).get_context_data(*args,**kwargs)
        all_category = ProductCategory.objects.all()
        cart_obj,new_obj = Cart.objects.create_or_get(request)
        special_deal = Product.objects.special_deal()
        special_offer = Product.objects.special_offer()
        context["cart_obj"] = cart_obj
        context["all_category"] = all_category
        context["special_deal"] = special_deal
        context["special_offer"] = special_offer
        return context

    def get_queryset(self,*args,**kwargs):
        request = self.request
        query = request.GET.get("q")
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.featured()
