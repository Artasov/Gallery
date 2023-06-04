import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .funcs import parse_xls_file_to_bd
from .models import Category, Product
from .serializers import ProductSerializer


@login_required(login_url='signin')
def upload_products(request):
    if not request.user.is_staff:
        return Http404

    if request.method != 'POST':
        return render(request, 'APP_shop/upload_products.html', {
            'categories': Category.objects.all()
        })

    xlsfile = request.FILES.get('xlsfile')
    category = request.POST.get('category')

    if not xlsfile or not category:
        return render(request, 'APP_shop/upload_products.html', {
            'categories': Category.objects.all(),
            'invalid': 'Либо файл либо категория выбраны неверно.'
        })

    parse_xls_file_to_bd(xlsfile, category)


def catalog(request):
    return render(request, 'APP_shop/catalog.html',
                  {'categories': Category.objects.all()})


def product_detail(request, id: int):
    product = get_object_or_404(Product, id=id, available=True)
    # cart_product_form = CartAddProductForm()
    return render(request, 'APP_shop/detail.html', {
        'product': product,
        # 'cart_product_form': cart_product_form
    })


@api_view(['GET'])
def get_favorite_products_bt_names(request):
    product_names = json.loads(request.GET.get('items'))
    if not product_names:
        Response(status=status.HTTP_404_NOT_FOUND)

    products_ = Product.objects.filter(name__in=product_names)
    serializer = ProductSerializer(products_, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_new_for_pagination(request, last_pag_num: int):
    category = request.query_params.get('category', '').strip().lower()
    metal = request.query_params.get('metal', '').strip().lower()

    products_all = Product.objects.filter(available=True)

    if Category.objects.filter(slug=category).exists():
        products_all = products_all.filter(category=Category.objects.get(slug=category))
    if metal == 'gold':
        products_all = products_all.filter(Q(proba='585') | Q(proba='375'))
    elif metal == 'silver':
        products_all = products_all.filter(Q(proba='925'))

    count = products_all.count()

    if count > last_pag_num + settings.PAGINATION_PRODUCT_COUNT:
        pag_part = products_all[last_pag_num:last_pag_num + settings.PAGINATION_PRODUCT_COUNT]
    elif count != last_pag_num:
        pag_part = products_all[last_pag_num:]
    else:
        return Response({'end': True}, status=status.HTTP_200_OK)

    serializer = ProductSerializer(pag_part, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
