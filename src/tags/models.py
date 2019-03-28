from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from products.models import Product
from products.utils import unique_product_slug_generator


class ProductTag(models.Model):
    title           = models.CharField(max_length=250)
    slug            = models.SlugField(unique=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    active          = models.BooleanField(default=True)
    tagged_product  = models.ManyToManyField(Product,blank=True)


    def __str__(self):
        return self.title 


def tag_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_product_slug_generator(instance)

pre_save.connect(tag_pre_save_receiver,sender=ProductTag)