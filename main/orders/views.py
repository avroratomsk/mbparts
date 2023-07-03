from django.shortcuts import render, redirect
from accounts.models import UserProfile

from shop.models import Product, ProductOption
from .models import OrderItem
from .forms import CallbackForm, OrderCreateForm
from cart.cart import Cart
from setup.models import ThemeSettings
from .telegram import order_telegram, send_message
from sms.views import send_sms
try:
    theme_address = ThemeSettings.objects.get().name
except:
    theme_address = 'default'


from pay.models import PaymentSet
try:
    pay_name = PaymentSet.objects.get().name
except:
    pay_name = 'none'


# print(pay_name)


if pay_name == 'yookassa':
    from pay.yookassa_pay import create_payment

if pay_name == 'alfabank':
    from pay.alfabank_pay import create_payment, get_status

if pay_name == 'paykeeper':
    from pay.paykeeper_pay import create_payment, get_status

if pay_name == 'tinkoff':
    from pay.tinkoff_pay import create_payment



def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        pay_method = request.POST['pay_method']


        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            

           
            try:
                user = UserProfile.objects.get(id=request.session['user_profile_id'])
                order.user = user
            except:
                user = None
                order.user = None

            order.summ = cart.get_total_price_after_discount()
            order.pay_method = pay_method

            try:
                email = request.POST['email']
                order.email = email
            except:
                pass
            try:
                first_name = request.POST['first_name']
                order.first_name = first_name
            except:
                pass
            try:
                last_name = request.POST['last_name']
                order.last_name = last_name
            except:
                pass
            try:
                phone = request.POST['phone']
                order.phone = phone
            except:
                pass

            order.save()


            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                    )
                
                pr = Product.objects.get(id=item['product'].id)

                # Добавляем продажу для учета хитов продаж
                sales_old = pr.sales
                sales_new = int(sales_old)+int(item['quantity'])

                pr.sales = sales_new

                # Отнимаем количество, если указано в настройках
                if pr.subtract == True:
                    pr.stock = pr.stock - item['quantity']
                    if pr.stock < 0:
                        pr.stock = 0

                    

                pr.save()

            for item in cart.get_zakaz():

                OrderItem.objects.create(
                    order=order,
                    zakaz_name=item['name'],
                    zakaz_supplier=item['supplier'],
                    price=str(item['price']).replace(',','.'),
                    quantity=item['quantity']

                    )
            

                
            if pay_method == 'Оплата картой на сайте':

                if pay_name == 'yookassa':
                    data = create_payment(order, cart, request)
                    payment_id = data['id']
                    confirmation_url = data['confirmation_url']

                    order.payment_id = payment_id
                    order.payment_dop_info = confirmation_url
                    order.save()
                    print(data['path'])
                    return redirect(confirmation_url)
                
            else:
                order_telegram(order)
                text = f'Ваш заказ принят. Ему присвоен № {order.id}.'
                
                send_sms(text, order.phone)

                cart.clear()
                # cart.zakaz_clear()

                return redirect('orders:thank')

            
    else:

        try:
            user_profile = UserProfile.objects.get(id=request.session['user_profile_id'])
            data = {
                'first_name': user_profile.first_name,
                'last_name': user_profile.last_name,
                'email': user_profile.email,

                'phone': user_profile.telephone,
                'apartment': user_profile.apartment,
                'address': user_profile.address,
                'postal_code': user_profile.postal_code,
                'city': user_profile.city,
            }
            form = OrderCreateForm(data)

        except Exception as e:
            print(e)
            form = OrderCreateForm()


 

    return render(request, 'global/create.html',
                  {'cart': cart, 'form': form})



def order_callback(request):
    if request.method == 'POST':

        form = CallbackForm(request.POST)
        name = request.POST['name']
        tel = request.POST['phone']
        messages = request.POST['messages']

        message = "Заказ обратного звонка:" + "\n" + "*ИМЯ*: " +str(name) + "\n" + "*ТЕЛЕФОН*: " + str(tel) + "\n" + "*СООБЩЕНИЕ*: " +str(messages)
        
        if form.is_valid():
            send_message(message)

            
            return redirect('orders:thank')


def thank(request):



    return render(request, 'global/created.html')





from orders.models import Order
from yookassa import Payment
def order_confirm(request, pk):
    cart = Cart(request)
    
    try:
        order = Order.objects.get(id=pk, paid=False, pay_method='Оплата картой на сайте')
        payment = Payment.find_one(order.payment_id)
        status = payment.status
        

        if status == 'succeeded':
            order_telegram(order)
            text = f'Ваш заказ принят. Ему присвоен № {order.id}.'
            send_sms(text, order.phone)
            cart.clear()
           
            order.paid = True
            order.save()

            return redirect('orders:thank')


        context = {
            'order': order,
            'status': status,
            
        }

        return render(request, 'orders/order/confirm.html', context)
    except:

        return redirect('home')

# Проверка событий Юкассы не работает
import logging
logger = logging.getLogger(__name__)
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from yookassa.domain.notification import WebhookNotification
@csrf_exempt
def order_webhook(request):
    if request.method == 'POST':
        event_json = json.loads(request.body)
            
        try:
            notification_object = WebhookNotification(event_json)
        except Exception as e:
            print(e)
          
        # Получите объекта платежа
        payment = notification_object.object
        logger.info(payment.id)
        pay_id = payment.id
        try:
            order = Order.objects.get(payment_id=pay_id, paid=False, pay_method='Оплата картой на сайте')
            payment = Payment.find_one(pay_id)
            status = payment.status
            if status == 'succeeded':
                
                order_telegram(order)
                text = f'Ваш заказ принят. Ему присвоен № {order.id}.'
                send_sms(text, order.phone)
                order.paid = True
                order.save()

     
                return HttpResponse(status=200)
        except Exception as e:
            logger.info(e)
            return HttpResponse(status=200)



def order_error(request):
    return render(request, 'orders/order/error.html')


def order_success(request):
    cart = Cart(request)

    pay_id = request.GET['orderId']

    data = get_status(pay_id)

    if data['status'] == '0':
        order = data['order']

        order_telegram(order)
        
        text = f'Ваш заказ принят. Ему присвоен № {order.id}.'
        send_sms(text, order.phone)

        
        cart.clear()
        request.session['delivery'] = 1
        order.paid = True
        
        order.save()

        return redirect('/?order=True')

    else:
        return redirect('orders:order_error')
