from django.http import JsonResponse,HttpResponse
from django.shortcuts import render,redirect
from django.utils.http import is_safe_url 
from billing.models import BillingProfile,Card
import stripe 





stripe.api_key = "sk_test_MaZ7xsOWriHe1wvPIvDkOwpW"
STRIPE_PUB_KEY = "pk_test_NW2dTXyWJD6CrGWqRLRmmZvA"

def payment_method_view(request):

    billingprofile,billingprofile_created = BillingProfile.objects.new_or_get(request)
    if not billingprofile:
        return redirect("/")
    
    next_url = None
    next_ = request.GET.get("next")
    if is_safe_url(next_,request.get_host()):
        next_url = next_

    template_name = "billing/payment-method.html"
    context = {
        "published_key":STRIPE_PUB_KEY,
        "next_url":next_url
    }
    return render(request,template_name,context)


def payment_method_create_view(request):

    if request.method == "POST" and request.is_ajax:
        billingprofile,billingprofile_created = BillingProfile.objects.new_or_get(request)
      
        
        token = request.POST.get("token")
        if token is not None:
            customer = stripe.Customer.retrieve(billingprofile.customer_id)
            card_response = customer.sources.create(source=token)
            new_card_object = Card.objects.add_new(billingprofile,card_response)
            print(new_card_object)
        return JsonResponse({"message":" Your card has been added."})
    else:
        return HttpResponse("Error")