from django.shortcuts import render,redirect
from django.utils.http import is_safe_url 
from django.contrib.auth import (
                                authenticate, 
                                login, 
                                get_user_model
                            )
from .forms import (
                    LoginForm,
                    Register,
                    GuestForm
                )
from .models import GuestEmail
from products.models import ProductCategory
            

User = get_user_model()

def login_views(request):
    template_name = "accounts/login.html"
    category = ProductCategory.objects.all()
    form = LoginForm(request.POST or None)
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None

    if request.user.is_authenticated:
        return redirect("/")
    else:
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect("/")
                try:
                    del request.session["guest_email_id"]
                except:
                    pass 
                    
                if is_safe_url(redirect_path,request.get_host()):
                    return redirect(redirect_path)
            else:
                print("Error")
    context = {
        "form":form,
        "all_category":category,
    }
    return render(request,template_name,context)


def guest_login_views(request):

    form = GuestForm(request.POST or None)
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None

    if form.is_valid():
        email = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session["guest_email_id"] = new_guest_email.id  
        if is_safe_url(redirect_path,request.get_host()):
                return redirect(redirect_path)
        else:
            return redirect("/")
    context = {
        "form":form
    }
    return redirect("accounts/register/")

def register_user(request):
    template_name = "accounts/register.html"
    category = ProductCategory.objects.all()
    form = Register(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("accounts:login")

    context = {
        "form":form,
        "all_category":category,
    }
    return render(request,template_name,context)

