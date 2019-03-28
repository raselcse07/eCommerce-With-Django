from django import template
from decimal import *
from products.models import Product


register = template.Library()

@register.filter()
def multiply(price,val):
    old_price = price + (Decimal(price) * Decimal(val))
    formatted_price = format(old_price,".2f")
    return formatted_price

@register.filter()
def count_product(category):
    return Product.objects.filter(category=category).count()

@register.filter()
def category_product(products,category):
    return products.filter(category=category)[2:20]


@register.filter()
def category_product_all(products,category):
    return products.filter(category=category)

@register.filter()
def category_1st_half(category):
    half= len(category) // 2
    return category[:half]

@register.filter()
def category_2nd_half(category):
    half= len(category) // 2
    return category[half:]
