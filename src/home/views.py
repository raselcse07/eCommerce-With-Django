from django.shortcuts import render
from products.models import (
                        Product,
                        ProductCategory
                    )
from cart.models import Cart

def home_page(request):

    # get latest arival product
    new_products = Product.objects.latest_arival()

    # get featured product 
    featured_product = Product.objects.featured()

    # get mens collections
    mens_collection = Product.objects.mens_collection()

    # get mens collections
    womens_collection = Product.objects.womens_collection()

    # get offer
    special_offer = Product.objects.special_offer()

    # get special deal
    special_deal = Product.objects.special_deal()

    # get cart object
    cart_obj,new_obj = Cart.objects.create_or_get(request)

    # get category
    category = ProductCategory.objects.all()


    template_name = "home/index.html"
    
    context = {
        "new_products":new_products,
        "featured_product":featured_product,
        "cart_obj":cart_obj,
        "mens_collection":mens_collection,
        "special_offer":special_offer,
        "womens_collection":womens_collection,
        "special_deal":special_deal,
        "all_category":category,
        "category_count":category.count()
    }

    return render(request,template_name,context)
