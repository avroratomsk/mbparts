from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon
from django.conf import settings
from accounts.models import UserProfile

# Create your models here.
from shop.models import Product, ProductOption
class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='user_order')
    first_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Фамилия')
    phone = models.CharField(max_length=50, null=True, blank=True, verbose_name='Телефон')
    email = models.EmailField(null=True, blank=True, verbose_name='E-mail')
    address = models.CharField(max_length=250, null=True, blank=True, verbose_name='Адрес')

    address_comment = models.CharField(max_length=250, null=True, blank=True, verbose_name='Комментарий к адресу')
    order_conmment = models.CharField(max_length=250, null=True, blank=True, verbose_name='Комментарий к заказу')
    

    postal_code = models.CharField(max_length=20, null=True, blank=True, verbose_name='Индекс')
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name='Город')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    delivery_method = models.CharField(max_length=250, null=True, blank=True, verbose_name='Способ доставки')

    payment_id = models.CharField(max_length=250, verbose_name="ID платежа", null=True, blank=True)
    payment_dop_info = models.CharField(max_length=550, verbose_name="Информация о платеже (ссылка на плптеж)", null=True, blank=True)

    paid = models.BooleanField(default=False)
    pay_method = models.CharField(max_length=250, verbose_name="Способ оплаты", null=True, blank=True)
    summ = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    STATUS_CLASS = (
       ('Новый', 'Новый'),
       ('В работе', 'В работе'),
       ('Обработан', 'Обработан'),
       ('Выполнен', 'Выполнен'),
       ('Отказ', 'Отказ')
    )
    status = models.CharField(max_length=250, verbose_name='Статус заказа', choices=STATUS_CLASS, default='Новый',)
    coupon = models.ForeignKey(Coupon,
                                    related_name='orders',
                                    null=True,
                                    blank=True, on_delete=models.CASCADE)
    discount = models.IntegerField(default=0,
                                        validators=[MinValueValidator(0),
                                                MaxValueValidator(100)])
    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, null=True, blank=True)
    zakaz_name = models.CharField(max_length=250, null=True, blank=True)
    zakaz_supplier = models.CharField(max_length=250, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

   
    def get_cost(self):
        return self.price * self.quantity