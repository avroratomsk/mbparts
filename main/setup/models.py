from venv import create
from django.db import models
from admin.singleton_model import SingletonModel

# Create your models here.

class BaseSettings(SingletonModel):
    name = models.CharField(max_length=350, blank=True, null=True)
    phone = models.CharField(max_length=250, blank=True, null=True)
    whatsapp = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    email_for_order = models.EmailField(blank=True, null=True)
    telegram_bot = models.CharField(blank=True, null=True, max_length=350)
    telegram_group = models.CharField(blank=True, null=True, max_length=350)
    work_time = models.CharField(max_length=250, verbose_name='Время работы', null=True, blank=True)
    copy_year = models.CharField(max_length=350, blank=True, null=True)
    copy = models.CharField(max_length=350, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    promo = models.CharField(max_length=500, blank=True, null=True)
    meta_title = models.CharField(max_length=350, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    text = models.TextField(null=True, blank=True)
    meta_keywords = models.CharField(max_length=350, blank=True, null=True)
    social_image = models.FileField(upload_to="social_image", blank=True, null=True)
    logo_light = models.FileField(upload_to="logo", blank=True, null=True)
    logo_dark = models.FileField(upload_to="logo", blank=True, null=True)
    icon_ico = models.FileField(upload_to="fav", blank=True, null=True)
    icon_png = models.FileField(upload_to="fav", blank=True, null=True)
    icon_svg = models.FileField(upload_to="fav", blank=True, null=True)
    theme_color = models.CharField(max_length=250, blank=True, null=True)
    active = models.BooleanField(default=False)
    debugging_mode = models.BooleanField(default=True)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)


    def get_phone(self):

        if self.phone:
            phone_str = self.phone
            phone_list = phone_str.split(',')
            
            print(phone_list)
            try:
                res_one = phone_list[0].replace(' ','').replace('-','').replace('(','').replace(')','')
                res_two = phone_list[1].replace(' ','').replace('-','').replace('(','').replace(')','')
                phone = f'<a href="tel:{ res_one }" class="header__mobile-phone">{phone_list[0]}</a> <a href="tel:{ res_two }" class="header__mobile-phone">{phone_list[1]}</a>'
            except:
                res_one = phone_list[0].replace(' ','').replace('-','').replace('(','').replace(')','')

                phone = f'<a href="tel:{ res_one }" class="header__mobile-phone">{phone_list[0]}</a>'
      


        else:
            
            base = BaseSettings.objects.get()
            phone = f'<a href="tel:{ base.get_phone() }" class="header-top__phone">{base.phone}</a>'

        return phone




class RecaptchaSettings(SingletonModel):
    recaptcha_private_key = models.CharField(max_length=250, blank=True, null=True)
    recaptcha_public_key = models.CharField(max_length=250, blank=True, null=True)
    recaptcha_default_action = models.CharField(max_length=250, default='generic', blank=True, null=True)
    recaptcha_score_threshold = models.CharField(max_length=250, default='0.5', blank=True, null=True)
    recaptcha_language = models.CharField(max_length=250, default='ru', blank=True, null=True)



class EmailSettings(SingletonModel):
    host = models.CharField(max_length=250, blank=True, null=True)
    host_user = models.CharField(max_length=250, blank=True, null=True)
    host_password = models.CharField(max_length=250, blank=True, null=True)
    host_from = models.CharField(max_length=250, blank=True, null=True)
    host_port = models.CharField(max_length=250, default='465', blank=True, null=True)
    use_ssl = models.BooleanField(default=True)
    use_tls = models.BooleanField(default=False)



class CustomCode(models.Model):
    name = models.CharField(max_length=250)
    code = models.TextField()
    h_f = models.BooleanField()




class ThemeSettings(SingletonModel):
    THEME_CLASS = (
       ('default', 'default'),
       ('mb', 'mb'),
       
    )
    name = models.CharField(max_length=250, choices=THEME_CLASS, default='default')
    


class Colors(SingletonModel):
    primary = models.CharField(max_length=50, default='#6934FF')
    secondary = models.CharField(max_length=50)
    success = models.CharField(max_length=50, default='#198754')
    danger = models.CharField(max_length=50, default='#dc3545')
    warning = models.CharField(max_length=50, default='#ffc107')
    info = models.CharField(max_length=50, default='#0dcaf0')