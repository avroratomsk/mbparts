from django.db import models
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress

# Create your models here.


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)


    first_name = models.CharField(max_length=250, verbose_name='Имя', null=True, blank=True)
    last_name = models.CharField(max_length=250, verbose_name='Фамилия', null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField('Телефон', max_length=50, blank=True, null=True, unique=True)
    
    password = models.CharField(max_length=250, verbose_name='Пароль', null=True)
    
    auto = models.CharField(max_length=250, verbose_name='Марка авто', null=True, blank=True)
    vin = models.CharField(max_length=250, verbose_name='VIN', null=True, blank=True)
 
    address = models.CharField(max_length=50, blank=True, null=True, verbose_name="улица, дом, квартира")
    apartment = models.CharField(max_length=20, blank=True, null=True, verbose_name="")

    postal_code = models.CharField(max_length=50, blank=True, null=True, verbose_name="Индекс")
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="Город")
    
    mod_date = models.DateTimeField('Last modified', auto_now=True)

    cart_code = models.CharField(max_length=250, verbose_name='Скидочная карта', null=True, blank=True)


    def get_phone(self):
        try:
            phone = self.telephone
            res = phone.replace(' ','').replace('-','').replace('(','').replace(')','').replace('+','')
        except:
            res = ''

        return res



    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return "{}'s profile".format(self.user.__str__())


    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False