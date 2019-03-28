from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.utils.http import is_safe_url 
from products.models import Product,ProductCategory
from billing.models import BillingProfile
from orders.models import Orders
from accounts.forms import (
                            LoginForm,
                            Register,
                            GuestForm
                        )
from accounts.models import GuestEmail
from address.models import Addresses
from address.forms import AddressForm
from .models import Cart 



def cart_update_api_view(request):
    cart_obj,new_obj = Cart.objects.create_or_get(request)
    product = [{"id":x.id,
                "url":x.get_absolute_url,
                "title":x.title,
                "price":x.price
            } for x in cart_obj.product.all()]
    cart_data = {
                "product":product,
                "sub_total":cart_obj.sub_total,
                "total":cart_obj.total
            }
    return JsonResponse(cart_data)


def cart_home(request):
    template_name = "cart/home.html"
    all_category = ProductCategory.objects.all()
    cart_obj,new_obj = Cart.objects.create_or_get(request)
    context = {
        "cart_obj":cart_obj,
        "all_category":all_category
    }
    return render(request,template_name,context)


def cart_update(request):
    product_id = request.POST.get("product_id")
    in_detail = request.POST.get("in_detail")

    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect("cart:cart-home")

        cart_obj,new_obj = Cart.objects.create_or_get(request)
        if product_obj in cart_obj.product.all():
            cart_obj.product.remove(product_obj)
            added = False
        else:
            cart_obj.product.add(product_obj)
            added = True
        request.session["cart_total"] = cart_obj.product.count()

        if request.is_ajax():
            json_data = {
                "added":added,
                "removed": not added,
                "cart_item_count":cart_obj.product.count()

            }
            return JsonResponse(json_data)

    return redirect("cart:cart-home")
 


def checkout_home(request):
    template_name = "cart/checkout.html"
    order_obj = None
   
    cart_obj,cart_created = Cart.objects.create_or_get(request)
    all_category = ProductCategory.objects.all()
    
    if cart_created or cart_obj.product.count() == 0:
        return redirect("cart:cart-home")

    login_form = LoginForm(request.POST or None)
    guest_form = GuestForm(request.POST or None)
    address_form = AddressForm(request.POST or None)
    billing_address_id = request.session.get("billing_address_id",None)
    shipping_address_id = request.session.get("shipping_address_id",None)
    billingprofile,billingprofile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None

    if billingprofile is not None:
        if request.user.is_authenticated:
            address_qs = Addresses.objects.filter(billing_profile=billingprofile)

        order_obj,order_obj_created = Orders.objects.new_or_get(billingprofile,cart_obj)
        
        if shipping_address_id:
            order_obj.shipping_address = Addresses.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address_id = Addresses.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()

    if request.method == "POST":
        is_done = order_obj.check_done()
        if is_done:
            did_charge,mgs = billingprofile.charge(order_obj)
            if did_charge:
                order_obj.mark_paid()
                request.session["cart_total"] = 0
                del request.session["cart_id"]
                if not billingprofile.user:
                    billingprofile.set_card_inactive()
                return redirect("cart:checkout-success")
            else:
                return redirect("cart:checkout")

    context = {
        "order_obj":order_obj,
        "billingprofile":billingprofile,
        "login_form":login_form,
        "guest_form" : guest_form,
        "address_form":address_form,
        "address_qs":address_qs,
        "all_category":all_category
    }

    return render(request,template_name,context)


def checkout_done(request):
    all_category = ProductCategory.objects.all()
    return render(request,"cart/checkout-done.html",{"all_category":all_category})
