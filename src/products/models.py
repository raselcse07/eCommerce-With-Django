import os
import random
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.db.models.signals import pre_save
from .utils import unique_product_slug_generator

def get_image_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext 

def upload_image_path(instance,filename):
    name, ext = get_image_ext(filename)
    new_filename = random.randint(1,3910209312)
    final_filename = "{new_filename}{ext}".format(
                        new_filename = new_filename,
                        ext = ext
                    )
    return "product/{new_filename}/{final_filename}".format(
                        new_filename = new_filename,
                        final_filename = final_filename
                    )


class ProductManager(models.Manager):

    def featured(self):
        return self.get_queryset().filter(
                    featured=True,
                    latest = False,
                    special_offer = False,
                    special_deal = False,
                    for_mens = False,
                    for_womens = False,
                    for_kids = False
                )[:3]

    def latest_arival(self):
        return self.get_queryset().filter(
                        featured = False,
                        latest = True,
                        special_offer = False,
                        special_deal = False,
                        for_mens = False,
                        for_womens = False,
                        for_kids = False
                    )[:3]


    def mens_collection(self):
        return self.get_queryset().filter(
                        featured = False,
                        latest= False,
                        special_offer = False,
                        special_deal = False,
                        for_mens = True,
                        for_womens = False,
                        for_kids = False
                    )[:3]

    def womens_collection(self):
        return self.get_queryset().filter(
                        featured = False,
                        latest= False,
                        special_offer = False,
                        special_deal = False,
                        for_mens = False,
                        for_womens = True,
                        for_kids = False
                    )[:8]

    def special_offer(self):
        return self.get_queryset().filter(
                        featured = False,
                        latest = False,
                        special_offer = True,
                        special_deal = False,
                        for_mens = False,
                        for_womens = False,
                        for_kids = False
                    )[:10]
    
    def special_deal(self):
        return self.get_queryset().filter(
                        featured = False,
                        latest = False,
                        special_offer = False,
                        special_deal = True,
                        for_mens = False,
                        for_womens = False,
                        for_kids = False
                    )[:5]


    def get_by_slug(self,slug):
        qs = self.get_queryset().filter(slug=slug)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self,query):
        lookup = (
                    Q(title__icontains=query) | 
                    Q(description__icontains=query) |
                    Q(producttag__title__icontains=query)
                )
        return self.get_queryset().filter(lookup).distinct()


class ProductCategory(models.Model):
    title           = models.CharField(max_length=250)
    slug            = models.SlugField(unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return str(self.title)

    @property
    def get_absolute_url(self):
        return reverse("products:category-detail",kwargs={"slug":self.slug})



class Product(models.Model):
    title           = models.CharField(max_length=250)
    slug            = models.SlugField(unique=True)
    category        = models.ForeignKey(ProductCategory,on_delete=models.CASCADE)
    description     = models.TextField()
    price           = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    product_image   = models.ImageField(
                        upload_to = upload_image_path,
                        null = True,
                        blank = True,
                    )
    featured        = models.BooleanField(default=False)
    latest          = models.BooleanField(default=False)
    active          = models.BooleanField(default=False)
    special_offer   = models.BooleanField(default=False)
    special_deal    = models.BooleanField(default=False)
    for_mens        = models.BooleanField(default=False)
    for_womens      = models.BooleanField(default=False)
    for_kids        = models.BooleanField(default=False)

    class Meta:
        ordering = ["-id"]

    objects = ProductManager()


    def __str__(self):
        return self.title 

    @property
    def get_absolute_url(self):
        return reverse("products:product-detail",kwargs={"slug":self.slug})


def product_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_product_slug_generator(instance)

pre_save.connect(product_pre_save_receiver,sender=Product)

def category_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_product_slug_generator(instance)

pre_save.connect(category_pre_save_receiver,sender=ProductCategory)