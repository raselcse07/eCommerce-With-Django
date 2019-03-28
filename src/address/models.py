from django.db import models
from billing.models import BillingProfile


ADDRESS_TYPE = (
    ("billing","Billing"),
    ("shipping","Shipping")
)

class Addresses(models.Model):
    billing_profile = models.ForeignKey(BillingProfile,on_delete=models.CASCADE)
    address_type    = models.TextField(max_length=250,choices=ADDRESS_TYPE)
    address_line_1  = models.TextField(max_length=250)
    address_line_2  = models.TextField(max_length=250,null=True,blank=True)
    city            = models.CharField(max_length=250)
    state           = models.CharField(max_length=250)
    postal_code     = models.CharField(max_length=250)
    country         = models.CharField(max_length=250)

    def __str__(self):
        return str(self.billing_profile)
