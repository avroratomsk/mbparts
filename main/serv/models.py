from django.db import models
from django.urls import reverse
from admin.singleton_model import SingletonModel

class ServSetup(SingletonModel):
    description = models.TextField(null=True, blank=True, verbose_name='Описание каталога')
    meta_h1 = models.CharField(max_length=350, null=True, blank=True, verbose_name='h1')
    meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name='Мета тайтл')
    meta_description = models.TextField(null=True, blank=True, verbose_name='Мета описание')
    meta_keywords = models.TextField(null=True, blank=True, verbose_name='Ключевые слова через запятую')
    image = models.ImageField(upload_to='serv', null=True, blank=True, verbose_name='Изображение')



# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=250, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    text = models.TextField(verbose_name='Текст')

    meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name='Мета тайтл')
    meta_description = models.TextField(null=True, blank=True, verbose_name='Мета описание')
    meta_keywords = models.TextField(null=True, blank=True, verbose_name='Ключевые слова через запятую')
    image = models.ImageField(upload_to='catalog', null=True, blank=True, verbose_name='Изображение')

    min_srok = models.CharField(max_length=250, verbose_name='Минимальный срок оказания услуги', null=True, blank=True)
    how = models.CharField(max_length=250, verbose_name='Способ оказания услуги (по записи/без записи)', null=True, blank=True)

    home = models.BooleanField(default=False, verbose_name='Главная страница')
    price = models.CharField(max_length=250, verbose_name='Цена', null=True, blank=True)

    slug = models.SlugField(unique=True)


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse("serv_detail", kwargs={"slug": self.slug})
    


class ServiceGroup(models.Model):
    parent = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='groups', verbose_name='Услуга')
    name = models.CharField(max_length=250, verbose_name='Наименование')

    def __str__(self):
        return self.name


class ServiceItem(models.Model):
    parent = models.ForeignKey(ServiceGroup, on_delete=models.CASCADE, related_name='items', verbose_name='Услуга')

    name = models.CharField(max_length=250, verbose_name='Наименование')
    min_srok = models.CharField(max_length=250, verbose_name='Минимальный срок оказания услуги', null=True, blank=True)
    price = models.CharField(max_length=250, verbose_name='Цена (текстовый формат)')


    def __str__(self):
        return self.name


