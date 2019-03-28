from django.conf import settings
from django.db import models
from django.db.models.signals import post_save,pre_save
from accounts.models import GuestEmail
import stripe




stripe.api_key = "sk_test_MaZ7xsOWriHe1wvPIvDkOwpW"


User = settings.AUTH_USER_MODEL 

class ChargeManager(models.Manager):

    def do(self,billing_profile,order_obj,card=None):
        card_obj = card
        if card_obj is None:
            card = billing_profile.card_set.filter(_default=True)

            if card.exists():
                card_obj = card.first()
        if card_obj is None:
            return False, "No card avilable"
       
        c = stripe.Charge.create(
            amount = int(order_obj.order_total * 100),
            currency = "usd",
            customer = billing_profile.customer_id,
            source = card_obj.stripe_id,
            metadata = {"order_id":order_obj.order_id}
        )

        new_charge_obj = self.model(
            billing_profile = billing_profile,
            stripe_id       = c.id,
            paid            = c.paid,
            refunded        = c.refunded,
            outcome         = c.outcome,
            outcome_type    = c.outcome['type'],
            seller_message  = c.outcome.get('seller_message'),
            risk_level      = c.outcome.get('risk_level')
        )
        new_charge_obj.save()
        return new_charge_obj.paid, new_charge_obj.seller_message



class CardManager(models.Manager):
    def all(self,*args,**kwgars):
        return self.get_queryset().filter(active=True)

    def add_new(self,billing_profile,stripe_card_response):
        if str(stripe_card_response.object) == "card":
            new_card = self.model(
                billing_profile = billing_profile,
                stripe_id = stripe_card_response.id, 
                brand = stripe_card_response.brand,
                country = stripe_card_response.country,
                exp_month = stripe_card_response.exp_month,
                exp_year = stripe_card_response.exp_year,
                last4 = stripe_card_response.last4,
            )
            new_card.save()
            return new_card
        return None


class BillingProfileManager(models.Manager):
    def new_or_get(self,request):
        user = request.user 
        guest_email_id = request.session.get("guest_email_id")
        obj = None
        created = False
        if user.is_authenticated:
            obj,created = self.model.objects.get_or_create(user=user,email=user.email)
        elif guest_email_id is not None:
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj,created = self.model.objects.get_or_create(email=guest_email_obj.email)
        else:
            pass
        return obj,created



class BillingProfile(models.Model):
    user            = models.ForeignKey(
                                        User,
                                        null=True,
                                        blank=True,
                                        unique=True,
                                        on_delete=models.CASCADE
                                    )
    email           = models.EmailField()
    customer_id     = models.CharField(max_length=220,null=True,blank=True)
    active          = models.BooleanField(default=True)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)


    objects = BillingProfileManager()

    def __str__(self):
        return self.email

    def charge(self,order_obj,card=None):
        return Charge.objects.do(self,order_obj,card)

    def get_cards(self):
        return self.card_set.all()
    
    @property
    def has_cards(self):
        card_qs = self.get_cards()
        return card_qs.exists()

    @property
    def default_cards(self):
        default_card = self.get_cards().filter(default=True)
        if default_card.exists():
            return default_card.first()
        return None


    def set_card_inactive(self):
        card_qs = self.get_cards()
        card_qs.update(active=False)
        return card_qs.filter(active=True).count()



class Card(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    stripe_id       = models.CharField(max_length=220,null=True,blank=True)
    brand           = models.CharField(max_length=220,null=True,blank=True)
    country         = models.CharField(max_length=20,null=True,blank=True)
    exp_month       = models.IntegerField(null=True,blank=True)
    exp_year        = models.IntegerField(null=True,blank=True)
    last4           = models.CharField(max_length=4,null=True,blank=True)
    _default        = models.BooleanField(default=True)
    active          = models.BooleanField(default=True)
    timestamp       = models.DateTimeField(auto_now_add=True)


    objects = CardManager()

    def __str__(self):
        return "{brand},{last4}".format(
            brand = self.brand,
            last4 = self.last4
        )


class Charge(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    stripe_id       = models.CharField(max_length=220,null=True,blank=True)
    paid            = models.BooleanField(default=False)
    refunded        = models.BooleanField(default=False)
    outcome         = models.TextField(null=True,blank=True)
    outcome_type    = models.CharField(max_length=20,null=True,blank=True)
    seller_message  = models.CharField(max_length=20,null=True,blank=True)
    risk_level      = models.CharField(max_length=20,null=True,blank=True)

    objects = ChargeManager()

    def __str__(self):
        return "{stripe_id},{paid}".format(
            stripe_id = self.stripe_id,
            paid = self.paid
        ) 


def billing_profile_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.customer_id and instance.email:
        customer = stripe.Customer.create(
            email = instance.email
        )
        instance.customer_id = customer.id
        print(customer)

pre_save.connect(billing_profile_pre_save_receiver,sender=BillingProfile)

def user_created_receiver(sender,instance,created,*args,**kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance,email=instance.email)

post_save.connect(user_created_receiver,sender=User)