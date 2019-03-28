from django.shortcuts import render,redirect
from django.utils.http import is_safe_url 
from billing.models import BillingProfile
from .forms import AddressForm
from .models import Addresses




def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {
        "form":form
    }
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None

    if form.is_valid():
        instance = form.save(commit=False)
        billingprofile,billingprofile_created = BillingProfile.objects.new_or_get(request)
        if billingprofile is not None:
            address_type = request.POST.get("address_type","shipping")
            instance.billing_profile = billingprofile
            instance.address_type = address_type
            instance.save()

            request.session[address_type + "_address_id"] = instance.id

        else:
            return redirect("cart:checkout")


        if is_safe_url(redirect_path,request.get_host()):
            return redirect(redirect_path)

    return redirect("cart:checkout")


def checkout_address_reuse_view(request):
    if request.user.is_authenticated:
        context = {}
        next_ = request.GET.get("next")
        next_post = request.POST.get("next")
        redirect_path = next_ or next_post or None
        
        if request.method == "POST":
            shipping_address = request.POST.get("shipping_address",None)
            address_type = request.POST.get("address_type","shipping") 
            billingprofile,billingprofile_created = BillingProfile.objects.new_or_get(request)
            if shipping_address is not None:
                qs = Addresses.objects.filter(billing_profile=billingprofile,id=shipping_address)
                if qs.exists():
                    request.session[address_type + "_address_id"] = shipping_address
            
                if is_safe_url(redirect_path,request.get_host()):
                    return redirect(redirect_path)

    return redirect("cart:checkout")
