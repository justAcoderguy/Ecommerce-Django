import re
from django.shortcuts import render
from inventory import models


def home(request):
    return render(request, 'index.html')


def category(request):

    data = models.Category.objects.all()

    return render(request, 'category.html', {"data": data})


def product_by_category(request, category):

    data = models.Product.objects.filter(category__slug=category).values(
        "id", "name", "slug", "category__name", "product__store_price",
        "product__product_inventory__units"
    )

    return render(request, 'product_by_category.html', {"data": data})


def product_detail(request, slug):

    filter_args = []

    if request.GET:
        for value in request.GET.values():
            filter_args.append(value)

    print(filter_args)
    from django.db.models import Count

    print(models.ProductInventory.objects.filter(product__slug=slug))

    # Returns the Default Product for all ProductInventory Tuples
    # See ProductInventory Model for more detail
    data = models.ProductInventory.objects.filter(product__slug=slug).filter(
        attribute_values__attribute_value__in=filter_args
    ).values(
        "id", "product__name", "sku", "store_price", "product_inventory__units"
    )

    return render(request, 'product_detail.html', {"data": data})
