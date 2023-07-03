from decimal import Decimal
from django.shortcuts import render
import requests
# Create your views here.
from bs4 import BeautifulSoup
import json
from pytils.translit import slugify

from shop.models import CharName, Manufacturer, Category, Product, ProductChar
from fake_useragent import UserAgent


# rossko

brand_url = ' https://api.berg.ru/v1.0/references/brands.json'
headers = {
    'User-Agent': UserAgent().chrome,
    
}




auth_token = '046b17fd0839c66f42a52b6dd83bb3639a3a50a790b0aee55fba8c9796214caf'

params = {
   'key': auth_token
}

# Получить список брендов
def get_berg():

    resp = requests.get(brand_url, params=params)
    
    # man_del = Manufacturer.objects.all()
    # man_del.delete()

    brands = resp.json()['brands']

    for brand in brands:

        id = 'berg_'+str(brand['id'])
        name = brand['name']
       

        try:
          
            model = Manufacturer.objects.create(
                id=id,
                name=name,
               
                )
            model.save()
            print(id)
        except Exception as e:
            print(id, e)
            

# get_berg()


import sys
import requests
import os

# Регистрация на сайте
def reg_berg(final_url):
    s = requests.Session()
    data = {"_username":"89048805003", "_password":"89048805003"}

    url = "https://berg.ru/login_check"
    r = s.post(url, data=data)

    s.cookies
    resp = s.get(final_url, stream=True)
    return resp


# Парсинг сайта
def get_cat():

    cat_del = Category.objects.all()
    cat_del.delete()
    prod_del = Product.objects.all()
    prod_del.delete()

    char_del = CharName.objects.all()
    char_del.delete()
    pr_del = ProductChar.objects.all()
    pr_del.delete()
    

    resp = reg_berg('https://berg.ru/products')
    soup = BeautifulSoup(resp.text, "lxml")
    parent_list = soup.find_all('ul', class_="catalog__list")
    for parent in parent_list:
        parent_name = parent.find('li', class_='title').text
        parent_slug = slugify(parent_name)
        try:
            parent_save = Category.objects.create(
                name=parent_name,
                slug=parent_slug,
                top=True
            )
        except:
            parent_save = Category.objects.get(slug=parent_slug)
        # print(parent_name, parent_slug)
        categorys = parent.find_all('li', class_='item')
        # print(categorys)
        counter = 0
        for item in categorys:
            item_name = item.find('a').text
            item_slug = slugify(item_name)
            item_url = item.find('a')['href']
            try:
                category_save = Category.objects.create(
                    name=item_name,
                    slug=item_slug,
                    parent=parent_save,
                    top=False
                )
            except Exception as e:
                category_save = Category.objects.get(slug=item_slug)

               
            cat_resp = reg_berg('https://berg.ru'+item_url)
            cat_soup = BeautifulSoup(cat_resp.text, "lxml")
            try:

                pagin_pages = cat_soup.find('div', class_='paginator').find('li', class_='ajax_link').find('a').text
            except Exception as e:
                pagin_pages = 1
            
            if pagin_pages == 1:
                pr_item = cat_soup.find_all('div', class_='search_result__row')
                
                

                for i in pr_item:
                    try:
                        product_name = i.find('span', class_='border').text
                        product_slug = slugify(product_name)
                        product_url = i.find('a', class_='pseudo_link part_description__link')['href']
                        brand_name = i.find('span', class_='brand_name').text
                        try:
                            manufacturer = Manufacturer.objects.get(name=brand_name)
                        except:
                            manufacturer = None
                        product_resp = reg_berg('https://berg.ru'+product_url)
                        product_soup = BeautifulSoup(product_resp.text, "lxml")
                        try:
                            price = Decimal(i.find_all('td', class_='price_col')[1].text.replace(',', '.').replace(' ', ''))
                            
                        except:
                            price = Decimal(i.find('td', class_='price_col').text.replace(',', '.').replace(' ', ''))
                        
                        print(product_name)
                        model = Product.objects.create(
                            name=product_name,
                            slug=product_slug,
                            price=price,
                            parent=category_save,
                            product_manufacturer=manufacturer,
                            provider = 'berg'
                        )

                        try:
                            thumb_url = product_soup.find('a', class_='preview_img__container').find('img')['data-src']
                            # print('https:'+thumb_url)
                            get_thumb = reg_berg('https:'+thumb_url)
                            thumb_name = thumb_url.split('/')[-1]
                            get_thumb.raw.decode_content = True
                            model.thumb.save(os.path.join('', thumb_name), get_thumb.raw)
                            model.save()
                        except Exception as e:
                            print(e)

                        groups = product_soup.find('div', class_='additional_info').find_all('div', class_='group')
                        sku = ''
                        for gr in groups:
                            rows_gr = gr.find_all('div', class_='row')
                            
                            for ch in rows_gr:
                                name = ch.find('div', class_='title_col').text.replace('  ', '')
                                value = ch.find('div', class_='value_col').text.replace('  ', '')

                                if name == 'Артикул':
                                    sku = value

                                if name != 'Разрешение производителя' and name != 'Наименование':

                                    try:
                                        ch_name = CharName.objects.get(text_name=name)
                                
                                    except:
                                        ch_name = CharName.objects.create(text_name=name)
                                    

                                    try:
                                        pr_char = ProductChar.objects.get(char_name=ch_name, char_value=value)
                                        pr_char.parent.add(model)
                                    except:
                                        pr_char = ProductChar.objects.create(char_name=ch_name, char_value=value)
                                        pr_char.parent.add(model)

                        model.sku = sku
                        model.save()

                    except Exception as e:
                        print(e)

                    counter += 1
                    print(counter)

            else:
                
                try:
                    count = 1
                    while count <= int(pagin_pages):

                        cat_resp_p = reg_berg('https://berg.ru'+item_url+'?page='+str(count))
                        cat_soup_p = BeautifulSoup(cat_resp_p.text, "lxml")
                        

                        print('https://berg.ru'+item_url+'?page='+str(count))
                        pr_item = cat_soup_p.find_all('div', class_='search_result__row')
                        
                        for i in pr_item:

                            try:
    
                                product_name = i.find('span', class_='border').text
                                product_slug = slugify(product_name)
                                
                                product_url = i.find('a', class_='pseudo_link part_description__link')['href']

                                brand_name = i.find('span', class_='brand_name').text

                                try:
                                    manufacturer = Manufacturer.objects.get(name=brand_name)
                                except:
                                    manufacturer = None

                                product_resp = reg_berg('https://berg.ru'+product_url)
                                product_soup = BeautifulSoup(product_resp.text, "lxml")

                                try:
                                    price = Decimal(i.find_all('td', class_='price_col')[1].text.replace(',', '.').replace(' ', ''))

                                except:
                                    price = Decimal(i.find('td', class_='price_col').text.replace(',', '.').replace(' ', ''))
                                
                                print(product_name)

                                model = Product.objects.create(
                                    name=product_name,
                                    slug=product_slug,
                                    price=price,
                                    parent=category_save,
                                    product_manufacturer=manufacturer,
                                    provider = 'berg'
                                )

                                try:
                                    thumb_url = product_soup.find('a', class_='preview_img__container').find('img')['data-src']
                                    get_thumb = reg_berg('https:'+thumb_url)
                                    thumb_name = thumb_url.split('/')[-1]
                                    get_thumb.raw.decode_content = True
                                    model.thumb.save(os.path.join('', thumb_name), get_thumb.raw)
                                    model.save()
                                except Exception as e:
                                    print(e)

                                groups = product_soup.find('div', class_='additional_info').find_all('div', class_='group')
                                sku = ''
                                for gr in groups:
                                    rows_gr = gr.find_all('div', class_='row')
                                    
                                    for ch in rows_gr:
                                        name = ch.find('div', class_='title_col').text.replace('  ', '')
                                        value = ch.find('div', class_='value_col').text.replace('  ', '')
                                        if name == 'Артикул':
                                            sku = value
                                        if name != 'Разрешение производителя' and name != 'Наименование':
                                            try:
                                                ch_name = CharName.objects.get(text_name=name)                             
                                            except:
                                                ch_name = CharName.objects.create(text_name=name)                                    
                                            try:
                                                pr_char = ProductChar.objects.get(char_name=ch_name, char_value=value)
                                                pr_char.parent.add(model)
                                            except:
                                                pr_char = ProductChar.objects.create(char_name=ch_name, char_value=value)
                                                pr_char.parent.add(model)
                            
                                model.sku = sku
                                model.save()

                            except Exception as e:
                                print(e)
                   
                        count += 1
                        counter += 1
                        print(counter)

                except Exception as e:
                    print(e)

# get_cat()



# Проверка наличия, цены и срока доставки
def get_check():

    products = Product.objects.filter(provider='berg')
   
    count = 0
    for product in products:
        
        try:
            resp = requests.get(f'https://api.berg.ru/ordering/get_stock.json?items[0][resource_article]={product.sku}&key'+auth_token, params=params)

            ofers = resp.json()['resources'][0]['offers']

            stock = 0
            price = []

            for ofer in ofers:
                stock = ofer['quantity']
                price.append({ofer['price']: stock})
            

            

            print(price)
            
            # product.stock = stock
            # product.price = min(price)
            # product.save()
        except:
            product.stock = 0
            product.save()


        count += 1


# get_check()


def man_count():
    man = Manufacturer.objects.all()
    print(man.count())


# man_count()