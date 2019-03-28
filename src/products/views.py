from django.shortcuts import render
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from cart.models import Cart
from .models import (
                    Product,
                    ProductCategory
                )


class CategoryDetail(DetailView):
    model = ProductCategory
    template_name = "products/category-detail.html"

    def get_context_data(self,*args,**kwargs):
        request = self.request
        context = super(CategoryDetail,self).get_context_data(*args,**kwargs)
        cart_obj,new_obj = Cart.objects.create_or_get(request)
        all_products = Product.objects.all()
        all_category = ProductCategory.objects.all()
        special_deal = Product.objects.special_deal()
        special_offer = Product.objects.special_offer()
        context["cart_obj"] = cart_obj
        context["all_products"] = all_products
        context["all_category"] = all_category
        context["special_deal"] = special_deal
        context["special_offer"] = special_offer
        return context



class FeaturedProductListView(ListView):
    template_name = "products/product-list.html"

    def get_queryset(self,*args,**kwargs):
        request = self.request
        return Product.objects.featured()

    def get_context_data(self,*args,**kwargs):
        request = self.request
        context = super(FeaturedProductListView,self).get_context_data(*args,**kwargs)
        all_category = ProductCategory.objects.all()
        cart_obj,new_obj = Cart.objects.create_or_get(request)
        special_deal = Product.objects.special_deal()
        special_offer = Product.objects.special_offer()
        context["cart_obj"] = cart_obj
        context["all_category"] = all_category
        context["special_deal"] = special_deal
        context["special_offer"] = special_offer
        return context


class ProductList(ListView):
    model = Product 
    template_name = "products/product-list.html"
    
    def get_context_data(self,*args,**kwargs):
        request = self.request
        context = super(ProductList,self).get_context_data(*args,**kwargs)
        all_category = ProductCategory.objects.all()
        cart_obj,new_obj = Cart.objects.create_or_get(request)
        special_deal = Product.objects.special_deal()
        special_offer = Product.objects.special_offer()
        context["cart_obj"] = cart_obj
        context["all_category"] = all_category
        context["special_deal"] = special_deal
        context["special_offer"] = special_offer
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = "products/product-detail.html"

    def get_context_data(self,*args,**kwargs):
        request = self.request
        context = super(ProductDetail,self).get_context_data(*args,**kwargs)
        cart_obj,new_obj = Cart.objects.create_or_get(request)
        all_products = Product.objects.all()
        all_category = ProductCategory.objects.all()
        context["cart_obj"] = cart_obj
        context["all_products"] = all_products
        context["all_category"] = all_category
        return context

    def get_object(self,*args,**kwargs):
        request = self.request 
        slug = self.kwargs.get("slug")
        instance = Product.objects.get_by_slug(slug)
        if instance is None:
            raise Http404("Product Does't Exists!")
        return instance
