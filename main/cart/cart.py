from decimal import Decimal
from django.conf import settings
from accounts.models import UserProfile
from shop.models import Product
from coupons.models import Coupon


class Cart(object):

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        try:
          user_profile = UserProfile.objects.get(id=request.session['user_profile_id'])

        except:
          user_profile = None

        # self.clear()

        # сохранение текущего примененного купона
        self.coupon_id = self.session.get('coupon_id')

        if user_profile and user_profile.cart_code:
            coupon = Coupon.objects.get(code=user_profile.cart_code)
            self.coupon_id = coupon.id

        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

        # Перебираем все ключи и ищем товары, которые были удалены 
        product_ids = self.cart.keys()
        empty = []
        for id in product_ids:
            try:
                prod = Product.objects.get(id=id)
              
            except:
                product = id
                empty.append(product)
        
        # Удаляем удаленные товары из корзины
        for em in empty:
            product = str(em)
            self.remove(product)

        zakaz = request.session.get('zakaz')

        if not zakaz:
            zakaz = self.session['zakaz'] = {
                '0': { 
                    'id': 0,
                    'name': 0,
                    'supplier': 0,
                    'quantity': 0,
                    'price': 0,
                    'date': 0
                }
            }

        self.zakaz = zakaz

    def add_zakaz(self, id, name, supplier, quantity, price, date):

        if id not in self.zakaz:

            self.zakaz[id] = {
                'id': id,
                'name': name,
                'supplier': supplier,
                'quantity': int(quantity),
                'price': str(price),
                'data': str(date)
                
                }

        else:
            
            self.zakaz[id]['quantity'] += int(quantity)
        
        self.session.modified = True


    def remove_zakaz(self, id):
        if id in self.zakaz:
            del self.zakaz[id]
            self.save()

    def plus_zakaz(self, id):
        self.zakaz[id]['quantity'] += 1
        self.save()
       


    def minus_zakaz(self, id):
        
        self.zakaz[id]['quantity'] -= 1

        if self.zakaz[id]['quantity'] == 0:
            del self.zakaz[id]
        self.save()


    def zakaz_clear(self):
        items = self.zakaz.keys()
        for item in list(items):
            if item != 0:
                del self.zakaz[item]
                self.save()

    def get_zakaz(self):

        zakaz_list = []

        for s in self.zakaz.values():
            if s['name'] != 0:
                zakaz_list.append(s)

        return zakaz_list
 
    def zakaz_summ(self):
        return sum((Decimal(str(item['price']).replace(',', '.')) * item['quantity']) for item in self.zakaz.values())

    def count_zakaz(self):
        zakaz_len = sum(int(item['quantity']) for item in self.zakaz.values())
        return zakaz_len
    

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                    'price': str(product.price),
                                    
                                    }

        # if product.subtract == True:

        if product.stock <= self.cart[product_id]['quantity'] + quantity:
            quantity = product.stock     
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        # else:
        #     self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def minus(self, product, quantity, update_quantity=False):
        
        product_id = str(product.id)
       
        self.cart[product_id]['quantity'] -= quantity

        if self.cart[product_id]['quantity'] == 0:
            if product_id in self.cart:
                del self.cart[product_id]
                self.save()

        self.save()


    def plus(self, product, quantity, update_quantity=False):
        
        product_id = str(product.id)
        
        if product.stock < self.cart[product_id]['quantity'] + quantity:
            quantity = product.stock     
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += 1
     
        self.save()
       

    def remove(self, product):
        
        """
        Удаление товара из корзины.
        """
        try:
            product_id = str(product.id)
        except:
            product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        
        for product in products:
            self.cart[str(product.id)]['product'] = product
        
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = (item['price']) * item['quantity']
           

            yield item


    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        count = sum(item['quantity'] for item in self.cart.values())

        return count + self.count_zakaz()



    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                self.cart.values()) + self.zakaz_summ()


    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True



    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()