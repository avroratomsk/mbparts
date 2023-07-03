from django.shortcuts import get_object_or_404, render
from .models import Category, Manufacturer, Product, ProductOption, ShopSetup, OptionType
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator
from cart.cart import Cart
import os
from setup.models import ThemeSettings
try:
    theme_address = ThemeSettings.objects.get().name
except:
    theme_address = 'default'


from .sort import func_sort
# Create your views here.


def catalog(request):
    # cart = Cart(request)
    # cart.clear()
    sort = request.GET.getlist('sort')
    limit = request.GET.getlist('limit')
    page_number = request.GET.get('page')
    man = request.GET.get('man')
    top = request.GET.get('top')
    manufacts = Manufacturer.objects.all().order_by('name')
    

    try:

        min_filter = Product.objects.all().order_by('price').first().price
        max_filter = Product.objects.all().order_by('-price').first().price
    except:
        
        min_filter = 0
        max_filter = 0

    
    try:
        min_price = request.GET['min_price']
    except:
        min_price = min_filter
    try:
        max_price = request.GET['max_price']
    except:
        max_price = max_filter

    
    


    product_list = Product.objects.filter(status=True, price__gte=min_price, price__lte=max_price, stock__gte=1).filter(price__gte=0).order_by(*sort)


    man_filter = request.GET.get('man_filter')
    if man_filter:
        man_list = str(man_filter).split(',')

        man_get_f = Manufacturer.objects.filter(name__in=man_list)
        product_list = product_list.filter(product_manufacturer__in=man_get_f)
    else:
        man_list = []
    

    products_man = Product.objects.filter(status=True, price__gte=min_price, price__lte=max_price, stock__gte=1)

    manufacts = Manufacturer.objects.filter(manufacturer_products__in=products_man).values('name').distinct()
    manufacts = manufacts.order_by('name')


    if man:
        man_list = []
        
        
        manuf = Manufacturer.objects.get(name=man)
        print(manuf)
        product_list = product_list.filter(product_manufacturer=manuf)


    if top:

        product_list = product_list.filter(top_collection=True)


    if limit:
        paginator = Paginator(product_list, *limit)
    else:
        paginator = Paginator(product_list, 16)


    page_number = request.GET.get('page')

    products = paginator.get_page(page_number)
    # products = func_sort(*sort, limit)

    context = {
        'products': products,
        'top': top,
        'shop_setup': ShopSetup.objects.get(),
        'manufacts': manufacts,
        'man_list': man_list,
        'sort': sort,
        'limit': limit,

        'min_filter': min_filter,
        'max_filter': max_filter,
        'min_price': min_price,
        'max_price': max_price
    }


    return render(request, 'shop/catalog.html', context)



def get_breadcrumbs(obj):
    breadcrumbs = []
    if obj.parent:
        breadcrumbs += get_breadcrumbs(obj.parent)
    breadcrumbs.append({'url': obj.get_absolute_url(), 'title': obj.name})
    return breadcrumbs




import re
from django.db.models import Q
def category_detail(request, slug):

    sort = request.GET.getlist('sort')
    limit = request.GET.getlist('limit')
    page_number = request.GET.get('page')

    category = get_object_or_404(Category, slug=slug)

    

    masla = False
    try:
        if category.parent.slug == 'masla-i-smazki':
            masla = True
        try:
            if category.parent.parent.slug == 'masla-i-smazki':
                masla = True
        except:
            pass
        
    except:
        if category.slug == 'masla-i-smazki':
            masla = True


    masla_list = []

    if masla == True:
        masla_list = [
            '0W-8',
            '0W-10',
            '0W-16',
            '0W-20',
            '0W-30',
            '0W-40',
            '5W-20',
            '5W-30',
            '5W-40',
            '5W-50',
            '10W-30',
            '10W-40',
            '10W-50',
            '10W-60',
            '15W-40',
            '15W-50',
            '20W-50',
            '75W',
            '75W-80',
            '75W-85',
            '75W-90',
            '75W-140',
            '80W-90',
            'LS',
            'LSD',
            'GL-3',
            'GL-4',
            'GL-5',
        ]

    
        volume_list = [
            '1л',
            '4л',
            '5л',
            '6л',
            '20л',
            '60л',
            '200л',
            '208л',
            '216л',
            '1кг',
            '5кг',
            '10кг',
            '20кг',
            '0.946л',
            '3.785л',
            '18.93л',
            'РОЗЛИВ'
        ]

    else:
        masla_list = []
        volume_list = []



    if category.children.count() > 0:
        subcats = Category.objects.filter(parent_id=category)
    else:
        subcats = Category.objects.filter(slug=slug)

    try:

        products_list = Product.objects.filter(status=True, parent__in=subcats)
        
        min_filter = products_list.order_by('price').first().price
        max_filter = products_list.order_by('-price').first().price
    except:
        products_list = []
        
        min_filter = 0
        max_filter = 0
        
    try:
        min_price = request.GET['min_price']
    except:
        min_price = min_filter
    try:
        max_price = request.GET['max_price']
    except:
        max_price = max_filter

    products_all = Product.objects.filter(status=True, parent__in=subcats, price__gte=min_price, price__lte=max_price, stock__gte=1)

    
    man_filter = request.GET.get('man_filter')
    if man_filter:
        man_list = str(man_filter).split(',')

        man_get_f = Manufacturer.objects.filter(name__in=man_list)
        products_all = products_all.filter(product_manufacturer__in=man_get_f)
    else:
        man_list = []
    

    products_man = Product.objects.filter(status=True, parent__in=subcats, price__gte=min_price, price__lte=max_price, stock__gte=1)

    manufacts = Manufacturer.objects.filter(manufacturer_products__in=products_man).values('name').distinct()
    manufacts = manufacts.order_by('name')

    try:
        masla_filter = request.GET['masla_filter']
    except:
        masla_filter = None

    if masla_filter:
        masla_filter_theme = masla_filter.split(',')
        # Разделяем значения masla_filter на отдельные строки и удаляем пустые значения
        masla_filter_list = filter(None, masla_filter.split(','))
        # Создаем объект Q для фильтрации товаров по значениям masla_filter
        q = Q()
        for value in masla_filter_list:
            q |= Q(name__icontains=value)
        # Применяем фильтр к текущему списку товаров
        products_all = products_all.filter(q)

        
    else:
        masla_filter_theme = []


    try:
        volume_filter = request.GET['volume_filter']
    except:
        volume_filter = None

    if volume_filter:
        volume_filter_theme = volume_filter.split(',')
        # Разделяем значения masla_filter на отдельные строки и удаляем пустые значения
        volume_filter_list = filter(None, volume_filter.split(','))
        # Создаем объект Q для фильтрации товаров по значениям masla_filter
        q = Q()
        for value in volume_filter_list:
            q |= Q(name__icontains=value)
        # Применяем фильтр к текущему списку товаров
        products_all = products_all.filter(q)

        
    else:
        volume_filter_theme = []
        


    products_all = products_all.order_by(*sort)


    if limit:
        paginator = Paginator(products_all, *limit)
    else:
        paginator = Paginator(products_all, 16)


    page_number = request.GET.get('page')

    products = paginator.get_page(page_number)

    breadcrumbs = get_breadcrumbs(category)


    context = {
        'masla': masla,
        'masla_list': masla_list,
        'masla_filter_theme': masla_filter_theme,
        'manufacts': manufacts,
        'man_list': man_list,
        'volume_list': volume_list,
        'volume_filter_theme': volume_filter_theme,
        'category': category,
        'products': products,
        'breadcrumbs': breadcrumbs,
        'shop_setup': ShopSetup.objects.get(),
        'sort': sort,
        'limit': limit,
        'min_filter': min_filter,
        'max_filter': max_filter,
        'min_price': min_price,
        'max_price': max_price
    }


    return render(request, 'shop/category_detail.html', context)


from itertools import groupby
def product_detail(request, parent, slug):
    product = get_object_or_404(Product, slug=slug, status=True, stock__gte=1)

    product_options = ProductOption.objects.filter(parent=product)

    products_op = []
    for pr in product_options:
        products_op.append(pr.id)

   

    types = OptionType.objects.filter(t_options__in=product_options)

    options_type = []
    for t in types:
        options_type.append(t.id)
    
    new_x = [el for el, _ in groupby(options_type)]

    filter_types = OptionType.objects.filter(id__in=new_x)

    
    similars = Product.objects.order_by("?").filter(parent_id=product.parent.id)[:8]

    try:
        option_second = ProductOption.objects.filter(parent=product)[1]
    except:
        option_second = []

    breadcrumbs = get_breadcrumbs(product)

    context = {
        'product': product,
        'breadcrumbs': breadcrumbs,
        'cart_product_form': CartAddProductForm(),
        'shop_setup': ShopSetup.objects.get(),
        'product_options': product_options,
        'similars':similars, 
        'products_op': products_op,
        'types': filter_types,
        'option_second': option_second
        }

    return render(request, 'shop/product_detail.html', context)