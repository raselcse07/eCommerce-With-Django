import math
from django.db import models
from django.db.models.signals import pre_save,post_save
from address.models import Addresses
from cart.models import Cart
from products.utils import unique_order_id_generator
from billing.models import BillingProfile



ORDER_STATUS_CHOICES=[
    ("created","Created"),
    ("paid","Paid"),
    ("shipped","Shipped"),
    ("refunded","Refunded"),
]

class OrderManager(models.Manager):

    def new_or_get(self,billingprofile,cart_obj):
        created = False
        order_qs = self.get_queryset().filter(
                                    cart = cart_obj,
                                    billing_profile = billingprofile,
                                    active=True,
                                    status="created"
                                    )
        if order_qs.count() == 1:
            order_obj = order_qs.first()
        else:
            order_obj= self.model.objects.create(cart = cart_obj,billing_profile = billingprofile)
            created = True
        return order_obj, created



class Orders(models.Model):
    billing_profile     = models.ForeignKey(BillingProfile,on_delete=models.CASCADE,null=True,blank=True)
    order_id            = models.CharField(max_length=250,blank=True)
    shipping_address    = models.ForeignKey(Addresses, related_name="shipping_address",null=True, blank=True,on_delete=models.CASCADE)
    billing_address     = models.ForeignKey(Addresses, related_name="billing_address", null=True, blank=True,on_delete=models.CASCADE)
    cart                = models.ForeignKey(Cart,on_delete=models.CASCADE)
    status              = models.CharField(max_length=250,default="created",choices=ORDER_STATUS_CHOICES)
    shipping_total      = models.DecimalField(decimal_places=2, max_digits=20, default=10.00)
    order_total         = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    active              = models.BooleanField(default=True)

    objects = OrderManager()


    def __str__(self):
        return self.order_id


    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total,shipping_total])
        formatted_total = format(new_total,".2f")
        self.order_total = formatted_total
        self.save()
        return new_total

    def check_done(self):
        billing_profile = self.billing_profile
        billing_address = self.billing_address
        shipping_address = self.shipping_address
        total = self.order_total 
        if billing_profile and billing_address and shipping_address and total > 0:
            return True
        return False

    def mark_paid(self):
        if self.check_done():
            self.status = "paid"
            self.save()
        return self.status


def order_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Orders.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)


pre_save.connect(order_pre_save_receiver,sender=Orders)


def post_save_order_total_receiver(sender,instance,created,*args,**kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Orders.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_order_total_receiver,sender=Cart)

def post_save_order(sender,instance,created,*args,**kwargs):
    if created:
        instance.update_total()
post_save.connect(post_save_order,sender=Orders)
