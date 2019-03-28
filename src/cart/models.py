from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models.signals import m2m_changed,pre_save 
from products.models import Product 
User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):

    def create_or_get(self,request):
        cart_id = request.session.get("cart_id",None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            cart_obj = qs.first()
            new_obj = False
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user 
                cart_obj.save()
        else:
            cart_obj = self.new(user=request.user)
            new_obj = True
            request.session["cart_id"] = cart_obj.id
        return cart_obj,new_obj


    def new(self,user=None):
        user_obj = None
        if user.is_authenticated:
            user_obj = user
        return self.get_queryset().create(user=user_obj)



class Cart(models.Model):
    user            = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    product         = models.ManyToManyField(Product,blank=True)
    sub_total       = models.DecimalField(decimal_places=2,max_digits=100,default=0.00)
    total           = models.DecimalField(decimal_places=2,max_digits=100,default=0.00)
    timestamp       = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    objects = CartManager()


    def __str__(self):
        return str(self.id)

def cart_m2m_changed_reciever(sender,instance,action,*args,**kwargs):
    if action == "post_add" or action == "post_remove" or action == "post_clear":
        products = instance.product.all()
        total = 0
        for x in products:
            total += x.price
        if instance.sub_total != total:
            instance.sub_total = total
            instance.save()  

m2m_changed.connect(cart_m2m_changed_reciever, sender=Cart.product.through)

def cart_pre_save_receiver(sender,instance,*args,**kwargs):
    if instance.sub_total > 0:
        instance.total = Decimal(instance.sub_total) * Decimal(1.08)
    else:
        instance.total = 0.00

pre_save.connect(cart_pre_save_receiver,sender=Cart)
