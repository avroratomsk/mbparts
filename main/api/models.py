from django.db import models

# Create your models here.



class Diapasone(models.Model):

    start = models.PositiveIntegerField(verbose_name='Начало диапазона')
    end = models.PositiveIntegerField(verbose_name='Конец диапазона')
    persent = models.PositiveIntegerField(verbose_name='Наценка')