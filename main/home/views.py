from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET
from django.http import HttpResponse
from .forms import VinForm
from shop.models import Product, Category
from setup.models import BaseSettings
from serv.models import Service
from .models import GalleryImage, Page, Reviews, Slider
from blog.models import Post
from setup.models import ThemeSettings

try:
    theme_address = ThemeSettings.objects.get().name
except:
    theme_address = 'default'

from django.views.generic import TemplateView, ListView

from api.berg import get_berg
from api.rossko import savePrice
from api.shate_m import get_search_results

# get_berg()

@require_GET
def robots_txt(request):
    try:
        setup = BaseSettings.objects.get()
        if setup.active == True:
            lines = [
                "User-Agent: *",
                "Disallow: /admin/",
                "Disallow: /order/",
                
                "Disallow: *utm=",
                "Allow: /static/*.css",
                "Allow: /static/*.js",
                "Allow: /static/*.png",
                "Allow: /static/*.jpg",
                "Allow: /static/*.gif",

                "User-Agent: Yandex",
                "Disallow: /admin/",
                "Disallow: /order/",
            
                "Disallow: *utm=",
                "Allow: /static/*.css",
                "Allow: /static/*.js",
                "Allow: /static/*.png",
                "Allow: /static/*.jpg",
                "Allow: /static/*.gif",

                "Clean-Param: utm_source&utm_medium&utm_campaign",
                "Host: example.com",
                "Sitemap: example.com/sitemap.xml",
            ]
        else:
            lines = [
                "User-Agent: *",
                "Disallow: /",
                
            ]

    except:
        lines = [
            "User-Agent: *",
            "Disallow: /",
            
        ]
        
    return HttpResponse("\n".join(lines), content_type="text/plain")




def page_not_found_view(request, exception):
    return render(request, 'global/404.html', status=404)

from cart.cart import Cart

def home(request):
    

    # posts = Post.objects.all()
    # posts.delete()


    # cart = Cart(request)
    # cart.clear()
    images = GalleryImage.objects.all()[:6]
    servs = Service.objects.all()
    news = Post.objects.filter(draft=False).order_by('-id')[:3]
    hit_products = Product.objects.all().order_by('-sales').exclude(stock__lte=0).exclude(thumb=None)[:8]
    # hit_products = Product.objects.all()[:8]
    slides = Slider.objects.all()
    reviews = Reviews.objects.all()
    context = {
        'categorys_home': Category.objects.filter(parent=None, status=True)[:9],
        'hit_products':hit_products,
        'slides': slides,
        'reviews': reviews,
        'servs': servs,
        'news': news,
        'images': images
    }
    
    return render(request, 'home/home.html', context)



def page_detail(request, slug):
    page = get_object_or_404(Page, type=slug)
    reviews = Reviews.objects.all()
    context = {
        'page': page,
        'reviews': reviews,
    }
    return render(request, 'home/page_detail.html', context)



from orders.telegram import send_message
def vin(request):

    if request.method == 'POST':
        form = VinForm(request.POST)
        if form.is_valid():
            fio = request.POST['fio']
            part = request.POST['part']
            phone = request.POST['phone']
            model = request.POST['model']
            vin = request.POST['vin']

            message = f'''Заявка с сайта. Запрос запчасти по VIN: 
                \n *ФИО*: {fio} 
                \n *Телефон*: {phone}
                \n *Запчасть*: {part}
                \n *Модель*: {model}
                \n *VIN/FRAME-код*: {vin}
                '''
            send_message(message)

            return redirect('orders:thank')
        
        else:

            return render(request, 'home/vin.html', {'vin_form': form})



    context = {
        
    }

    return render(request, 'home/vin.html', context)


from django.core.paginator import Paginator
def gallery(request):

    images_list = GalleryImage.objects.all()

    paginator = Paginator(images_list, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)


    context = {
        'images': page_obj
    }

    return render(request, 'home/gallery.html', context)

import re
from api.rossko import rossko_search
from api.shate_m import get_search_results


from django.db.models import Q

def split_string(string):
    alpha_part = ''
    digit_part = ''
    for char in string:
        if char.isalpha():
            alpha_part += char
        elif char.isdigit():
            digit_part += char
    return alpha_part, digit_part


def search(request):
    
    query = request.GET.get('q')
    
   

    # try:
    #     shate_m = mxgroup_search(query)
    # except:
    #     shate_m = []
    
    # print(shate_m)

    
    # print(result)
    

    context = {
        'query': query
    }
    return render(request, 'home/search.html', context)


import json
from django.http import HttpResponse

def search_rossko(request):
    if request.method == 'GET':

        query = request.GET.get('q')
        try:
            rossko = rossko_search(query)
        except:
            rossko = []

        response_data = json.dumps(rossko, ensure_ascii=False)
        return HttpResponse(response_data, content_type='application/json')


def search_shate_m(request):
    if request.method == 'GET':

        query = request.GET.get('q')
        try:
            shate_m = get_search_results(query)
        except Exception as e:
            print(e)
            shate_m = []

        response_data = json.dumps(shate_m, ensure_ascii=False)
        # print(response_data)
        return HttpResponse(response_data, content_type='application/json')
    


from api.favorit import get_favorit_get
def search_favorit(request):
    if request.method == 'GET':

        query = request.GET.get('q')
        try:
            get_favorit = get_favorit_get(query)
        except Exception as e:
            print(e)
            get_favorit = []

        response_data = json.dumps(get_favorit, ensure_ascii=False)
        # print(response_data)
        return HttpResponse(response_data, content_type='application/json')