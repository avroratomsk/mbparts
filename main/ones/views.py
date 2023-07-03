from decimal import Decimal
import io
from django.shortcuts import render
import csv
import pandas as pd
from shop.models import Category, Product, Manufacturer
import os.path
import os
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files import File
from pytils.translit import slugify
from django.core.files.storage import default_storage
import shutil
from django.conf import settings
from django.db.models import Count
# from .path_ones import path
from django.core.files.images import ImageFile
# Create your views here.
def delete_empty_categories():
    root_categories = Category.objects.filter(parent=None)
    for root_category in root_categories:
        if not has_products(root_category):
            delete_category_and_children(root_category)


def has_products(category):
    if category.products.exists():
        return True

    for child in category.children.all():
        if has_products(child):
            return True

    return False


def delete_category_and_children(category):
    for child in category.children.all():
        delete_category_and_children(child)

    category.delete()




def ones():


    # man_del = Manufacturer.objects.all()
    # man_del.delete()

    

    

    # prod = Product.objects.all()
    # prod.delete()

    prods = Product.objects.all()

    for prod in prods:
        prod.stock = 0
        prod.save()
    

    with open(f'{path}files/1cExchange.txt', encoding='utf-8') as f:
        
        
        s = ' '.join(f.read().splitlines())
       
        f = open(f'{path}files/replace.csv','w', encoding='utf-8')
        f.write(s.replace('\;/', '&&').replace(';', ', ').replace('&&', ';').replace(';\@/', "\n").replace('<>', ''))
        f.close()



    with open(f"{path}files/replace.csv", newline='\n', encoding='utf-8') as r_file:

        
        file_reader = csv.reader(r_file, delimiter = ";")

        count = 0
        for row in file_reader:
            
            pr_name = row[0].rstrip()
            pr_slug = slugify(pr_name)

            desc = row[3]
            quantity = row[2]
            image = row[5]
            brand_name = row[6].rstrip()
            brand_slug = slugify(brand_name)
            

            price = ''.join([x for x in row[4] if x.isdigit()])

            if price == '':
                price = 0

            cat_name = row[7].rstrip()
            cat_slug = slugify(cat_name)


            try:
                manufact = Manufacturer.objects.get(slug=brand_slug)
            except:
                if brand_name != '':
                    manufact = Manufacturer.objects.create(
                        name=brand_name,
                        slug=brand_slug,
  
                        )
                else:
                    manufact = None

            cats_list = []
            cat_name_count = 7
            while cat_name_count <= 9:
                try:
                    cat_l = row[cat_name_count]
                    if cat_l != '':
                        cats_list.append(cat_l.rstrip())
                    
                except:
                    pass

                cat_name_count += 1                

            
            # print(cats_list)

            pa = None
            top = True
            count = 0
            for a in reversed(cats_list):
                cat_slug = slugify(a)
                try:
                    cat_s = Category.objects.get(slug=cat_slug)
                    parent = pa
                    cat_s.save()
                    pa = cat_s
                    top = False
                except:
       
                    cat_s = Category(
                        parent = pa,
                        name=a,
                        slug=cat_slug,
                        top=top
                        )
                    cat_s.save()

                    pa = cat_s
                    top = False
            


            extensions = ['jpg', 'jpeg', 'png']
            dst = None
            image_path = None

            for i in range(1, 30):
                for ext in extensions:
                    file_path = f'{path}files/{image}_{i}.{ext}'
                    if os.path.exists(file_path):                              
                        thumb = file_path
                        dst = f'{path}media/products/thumb/{image}_{i}.{ext}'
                        shutil.copyfile(thumb, dst)
                        image_path = f'products/thumb/{image}_{i}.{ext}'
                
            try:
                product = Product.objects.get(ones_art=image)
                product.name=pr_name
                
                product.description=desc
                product.stock=quantity
             
                product.product_manufacturer=manufact
                product.parent=cat_s
                product.thumb = image_path
                product.price = price

                product.save()

            except Exception as e:
                print(e)
               
                product = Product.objects.create(
                    name=pr_name,
                    ones_art=image,
                    slug=pr_slug,
                    description=desc,
                    stock=quantity,
                    
                    product_manufacturer=manufact,
                    parent=cat_s,
                    thumb = image_path,
                    price = price
                    
                    )
                
                product.save()
    
    delete_empty_categories()
              

# ones()