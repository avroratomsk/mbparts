from decimal import Decimal
from distutils.log import debug
from itertools import product
from multiprocessing import context
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from admin.forms import AlfaBankForm, CouponForm, CategoryForm, CharGroupForm, CharNameForm, ColorsForm, DiapasoneForm, GalleryImageForm, OptionTypeForm, PayKeeperForm, PaymentForm, PostBlockForm, ProductCharForm, ProductForm, ManufacturerForm, ProductImageForm, ProductOptionForm, RecaptchaSettingsForm, ReviewsForm, ServSetupForm, ServiceForm, SetupForm, EmailSettingsForm, ShopSetupForm, ThemeSettingsForm, BlogCategoryForm, PostForm, SliderSetupForm, SliderForm, PageForm, OrderForm, BlogSetupForm, TinkoffForm, YookassaForm
from coupons.models import Coupon
from home.models import GalleryImage, Page, Reviews, Slider, SliderSetup
from accounts.models import UserProfile
from api.models import Diapasone

from orders.models import Order
from shop.models import Category, CharGroup, CharName, Manufacturer, OptionImage, Product, OptionType, ProductChar, ProductImage, ProductOption, ShopSetup
from setup.models import BaseSettings, Colors, CustomCode, EmailSettings, RecaptchaSettings, ThemeSettings
from blog.models import BlogCategory, BlogSetup, Post, PostBlock
from serv.models import ServSetup, Service, ServiceGroup, ServiceItem
from pay.models import PayKeeper, PaymentSet, Tinkoff, Yookassa, AlfaBank

import subprocess
from main.settings import RESET_FILE

from django.contrib.auth import get_user_model
User = get_user_model()

from django.db.models import Q

from django.contrib.auth.decorators import user_passes_test

from django.db.models import Sum


# Сессия с хранением состояния сайдбара в админке
@user_passes_test(lambda u: u.is_superuser)
def sidebar_show(request): 
   
    request.session['sidebar'] = 'True' 
    
    return redirect('admin')

@user_passes_test(lambda u: u.is_superuser)
def sidebar_hide(request): 
    
    request.session['sidebar'] = 'False' 
    return redirect('admin')


@user_passes_test(lambda u: u.is_superuser)
def admin(request):
    try:
        setup = BaseSettings.objects.get()
        shop_setup = ShopSetup.objects.get()
        blog_setup = BlogSetup.objects.get()
        email = EmailSettings.objects.get()
        theme = ThemeSettings.objects.get()
        colors = Colors.objects.get()
    except:
        setup = BaseSettings()
        shop_setup = ShopSetup()
        blog_setup = BlogSetup()
        email = EmailSettings()
        theme = ThemeSettings()
        colors = Colors()
        colors.save()
        theme.save()
        email.save()
        setup.save()
        shop_setup.save()
        blog_setup.save()


    products = Product.objects.all().count()
    orders = Order.objects.all().count()
    sales = Order.objects.all().aggregate(Sum('summ'))

    summ = sales['summ__sum']
    
    clients = User.objects.filter(is_superuser=False).count()
    products = Product.objects.all().count()
    
    context = {
        'products': products,
        'orders': orders,
        'summ': summ,
        'clients': clients,
    }

    return render(request, 'pages/index.html', context)



@user_passes_test(lambda u: u.is_superuser)
def general_settings(request):

    # Пытаемся выбрать модели настроек, если не получается - создаем новые. (для первого захода на сайт)
    try:
        setup = BaseSettings.objects.get()
        email = EmailSettings.objects.get()
        recaptcha = RecaptchaSettings.objects.get()
    except:
        setup = BaseSettings()
        email = EmailSettings()
        recaptcha = RecaptchaSettings()
        email.save()
        setup.save()
        recaptcha.save()

    # Сохранение основных настроек
    if request.method == 'POST':
        new_form = SetupForm(request.POST, request.FILES, instance=setup)
        if new_form.is_valid():
            new_form.save()

            subprocess.call(["touch", RESET_FILE])

            return redirect ('general_settings')

    # Заполнение форм значениями, для отображения уже сохраненных настроек
    setup = BaseSettings.objects.get()
    email = EmailSettings.objects.get()
    recaptcha = RecaptchaSettings.objects.get()
    
    form = SetupForm(instance=setup)
    email_form = EmailSettingsForm(instance=email)
    recaptcha_form = RecaptchaSettingsForm(instance=recaptcha)
    context = {
        'form': form,
        'setup': setup,
        'email_form': email_form,
        'recaptcha_form': recaptcha_form,
    }
    return render(request, 'settings/general_settings.html', context)



# Настройки почты POST
@user_passes_test(lambda u: u.is_superuser)
def email_settings(request):
    if request.method == 'POST':
        form = EmailSettingsForm(request.POST)
        if form.is_valid():
            form.save()

            subprocess.call(["touch", RESET_FILE])
            return redirect('general_settings')


# Настройки recaptcha POST
@user_passes_test(lambda u: u.is_superuser)
def recaptcha_settings(request):
    if request.method == 'POST':
        form = RecaptchaSettingsForm(request.POST)
        if form.is_valid():
            form.save()
            subprocess.call(["touch", RESET_FILE])
            return redirect('general_settings')


# Настройки кастомных кодов POST/GET
@user_passes_test(lambda u: u.is_superuser)
def codes_settings(request):
    if request.method == 'POST':
        name = request.POST['name']
        code = request.POST['code']
        
        try:
            h_f = request.POST['h_f']
            header = True
        except:
            header = False

        code = CustomCode(name=name, code=code, h_f=header)
        code.save()

        return redirect('codes_settings')


    codes = CustomCode.objects.all()
    context = {
        'codes': codes,
    }


    return render(request, 'settings/codes_settings.html', context)


# Удаление счетчиков. 
# !!! Редактирование пока убрал (нет формы в темплейте), потому что какой-то косяк в TextField при сохранении. По возможности поправить !!!
@user_passes_test(lambda u: u.is_superuser)
def codes_settings_edit(request, pk):
    if request.method =='POST':
        name = request.POST['name']
        code = request.POST['code']
        print(code)
        try:
            h_f = request.POST['h_f']
            header = True
        except:
            header = False
        code = CustomCode.objects.get(id=pk)
        code.name = name
        code.code = code
        code.h_f = header
        code.save()


        return redirect('codes_settings')

    else:
        code = CustomCode.objects.get(id=pk)
        code.delete()

        return redirect('codes_settings')


# Настройки цвета
@user_passes_test(lambda u: u.is_superuser)
def color_settings(request):

    if request.method == 'POST':
        form = ColorsForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect('color_settings')
    try:
        color = Colors.objects.get()
        form = ColorsForm(instance=color)
    except:
        form = ColorsForm()
    context = {
        'form': form
    }

    return render(request, 'settings/color_settings.html', context)


# Настройка темы
@user_passes_test(lambda u: u.is_superuser)
def theme_settings(request):
    if request.method == 'POST':

        form = ThemeSettingsForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect('theme_settings')

    try:
        theme = ThemeSettings.objects.get()
        form = ThemeSettingsForm(instance=theme)
    except:
        form = ThemeSettingsForm()
    
    context = {
        'form': form
    }

    return render(request, 'settings/theme_settings.html', context)




# Способы оплаты
@user_passes_test(lambda u: u.is_superuser)
def add_pay_method(request):
    if request.method == 'POST':
        form = PayMethodForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('shop_settings')
        else:
            return render(request, 'shop/pay_method/add_pay_method.html', {'form':form})
    form = PayMethodForm()
    context = {
        'form': form
    }
    return render(request, 'shop/pay_method/add_pay_method.html', context)


@user_passes_test(lambda u: u.is_superuser)
def edit_pay_method(request, pk):
    method = PayMethod.objects.get(id=pk)
    if request.method == 'POST':
        form = PayMethodForm(request.POST, request.FILES, instance=method)
        if form.is_valid():
            form.save()
            return redirect('shop_settings')
        else:
            return render(request, 'shop/pay_method/add_pay_method.html', {'form':form})
    form = PayMethodForm(instance=method)
    context = {
        'form': form
    }
    return render(request, 'shop/pay_method/add_pay_method.html', context)

@user_passes_test(lambda u: u.is_superuser)
def delete_pay_method(request, pk):
    method = PayMethod.objects.get(id=pk)
    method.delete()
    return redirect('shop_settings')


# Настроки платежей
@user_passes_test(lambda u: u.is_superuser)
def admin_payments(request):

    # payment = PaymentSet.objects.get()
    # PaymentSet.delete()

    if request.method == 'POST':

        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            subprocess.call(["touch", RESET_FILE])
            return redirect('admin_payments')
        else:
            return render(request, 'settings/admin_payments.html', {'form':form})


    try:
        payment = PaymentSet.objects.get()
        form = PaymentForm(instance=payment)

    except:
        payment = None
        form = PaymentForm()


    try:
        yookassa = Yookassa.objects.get()
        yookassa_form = YookassaForm(instance=yookassa)
    except:
        yookassa_form = YookassaForm()


    try:
        alfabank = AlfaBank.objects.get()
        alfabank_form = AlfaBankForm(instance=alfabank)
    except:
        alfabank_form = AlfaBankForm()


    try:
        paykeeper = PayKeeper.objects.get()
        paykeeper_form = PayKeeperForm(instance=paykeeper)
    except:
        paykeeper_form = PayKeeperForm()

    try:
        tinkoff = Tinkoff.objects.get()
        tinkoff_form = TinkoffForm(instance=tinkoff)
    except:
        tinkoff_form = TinkoffForm()


    context = {
        'payment': payment,
        'form': form,
        'yookassa_form':yookassa_form,
        'alfabank_form': alfabank_form,
        'paykeeper_form': paykeeper_form,
        'tinkoff_form': tinkoff_form

    }

    return render(request, 'settings/admin_payments.html', context)


@user_passes_test(lambda u: u.is_superuser)
def yookassa_save(request):

    if request.method == 'POST':
        yookassa_form = YookassaForm(request.POST)
        if yookassa_form.is_valid():
            yookassa_form.save()
            subprocess.call(["touch", RESET_FILE])
            return redirect('admin_payments')

        else:
            return redirect('admin_payments')


    else:
        return redirect('admin_payments')


@user_passes_test(lambda u: u.is_superuser)
def alfabank_save(request):

    if request.method == 'POST':
        alfabank_form = AlfaBankForm(request.POST)
        if alfabank_form.is_valid():
            alfabank_form.save()
            subprocess.call(["touch", RESET_FILE])
            return redirect('admin_payments')

        else:
            return redirect('admin_payments')


    else:
        return redirect('admin_payments')


@user_passes_test(lambda u: u.is_superuser)
def paykeeper_save(request):

    if request.method == 'POST':
        paykeeper_form = PayKeeperForm(request.POST)
        if paykeeper_form.is_valid():
            paykeeper_form.save()
            subprocess.call(["touch", RESET_FILE])
            return redirect('admin_payments')

        else:
            return redirect('admin_payments')


    else:
        return redirect('admin_payments')
    

@user_passes_test(lambda u: u.is_superuser)
def tinkoff_save(request):

    if request.method == 'POST':
        paykeeper_form = TinkoffForm(request.POST)
        if paykeeper_form.is_valid():
            paykeeper_form.save()
            subprocess.call(["touch", RESET_FILE])
            return redirect('admin_payments')

        else:
            return redirect('admin_payments')


    else:
        return redirect('admin_payments')
    




# !!! МАРКЕТИНГ !!!
# Промокоды
@user_passes_test(lambda u: u.is_superuser)
def admin_promo(request):

    context = {
        'coupons': Coupon.objects.all().order_by('valid_to')
    }

    return render(request, 'marketing/promo.html', context)

@user_passes_test(lambda u: u.is_superuser)
def promo_add(request):

    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('admin_promo')

    form = CouponForm()
    context = {
        'form': form
    }

    return render(request, 'marketing/promo_add.html', context)

@user_passes_test(lambda u: u.is_superuser)
def promo_edit(request, pk):
    coupon = Coupon.objects.get(id=pk)

    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()

            return redirect('admin_promo')

        else:
            return render(request, 'marketing/promo_edit.html', {'form':form})

    form = CouponForm(instance=coupon)
    context = {
        'form': form,
        'coupon': coupon
    }

    return render(request, 'marketing/promo_edit.html', context)

@user_passes_test(lambda u: u.is_superuser)
def promo_delete(request, pk):
    coupon = Coupon.objects.get(id=pk)
    coupon.delete()
    return redirect('admin_promo')




# !!! end МАРКЕТИНГ !!!




# !!! Продажи !!!

# Заказы
@user_passes_test(lambda u: u.is_superuser)
def admin_order(request):
    orders = Order.objects.all().order_by('-created')
    context = {
        'orders': orders
    }


    return render(request, 'order/admin_order.html', context)

@user_passes_test(lambda u: u.is_superuser)
def order_detail(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    context = {
        'order': order,
        'form': form,
    }


    return render(request, 'order/order_detail.html', context)


@user_passes_test(lambda u: u.is_superuser)
def order_status_change(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()

            return redirect('order_detail', order.id)


@user_passes_test(lambda u: u.is_superuser)
def order_delete(request, pk):
    order = Order.objects.get(id=pk)
    order.delete()
    return redirect('admin_order')
# !!! end Продажи !!!




# !!!!! МАГАЗИН !!!!! 

@user_passes_test(lambda u: u.is_superuser)
def shop_settings(request):
    try:
        shop_setup = ShopSetup.objects.get()
        form = ShopSetupForm(instance=shop_setup)
    except:
        form = ShopSetupForm()

    if request.method == 'POST':
        shop_setup = ShopSetup.objects.get()
        form_new = ShopSetupForm(request.POST, request.FILES, instance=shop_setup)
        if form_new.is_valid():
            form_new.save()

            return redirect('shop_settings')

        else:
            return render(request, 'shop/settings.html', {'form': form})




    context = {
        'form': form
    }

    return render(request, 'shop/settings.html', context)


# Список категорий
@user_passes_test(lambda u: u.is_superuser)
def admin_category(request):
    q = request.GET.get('q')
    sort = request.GET.getlist('sort')
    try:
        sort_t = sort[0]
    except:
        sort_t = sort
    
    try:
        categorys = Category.objects.filter(Q(name__icontains=q)).order_by(*sort)
    except:
        categorys = Category.objects.all().order_by('sort_order')
    context = {
        # Разрешить поиск на странице
        'search': 'search',
        'categorys': categorys,
        'q': q,
        'sort': sort_t,
    }
    return render(request, 'shop/category/category.html', context)


@user_passes_test(lambda u: u.is_superuser)
def cat_orderby_edit(request, pk):


    category = Category.objects.get(id=pk)

    if request.method == 'POST':
        order_by = request.POST['order']
        category.sort_order = order_by
        category.save()
    
    
        return redirect('admin_category')

# Добавление категорий
@user_passes_test(lambda u: u.is_superuser)
def category_add(request):
    if request.method == 'POST':
        form_new = CategoryForm(request.POST, request.FILES)
        if form_new.is_valid():
            name = request.POST['name']
            description = request.POST['description']
            meta_title = request.POST['meta_title']
            meta_description = request.POST['meta_description']
            meta_keywords = request.POST['meta_keywords']
            parent = request.POST['parent']
            try:
                # Пытаемся получить изображение
                image = request.FILES['image']
            except:
                # Если не выходит, ставим что его нет
                image = None
            try:
                # Пытаемся получить положительное значение чекбокса "Отображение в меню"
                top = request.POST['top']
                top = True
            except:
                # Если не выходит, ставим отрицательное
                top = False
            column = request.POST['column']
            sort_order = request.POST['sort_order']
            try:
                # Пытаемся получить положительное значение чекбокса "Статус"
                status = request.POST['status']
                status = True
            except:
                # Если не выходит, ставим отрицательное
                status = False
            slug = request.POST['slug']
            cat = Category(
                name=name,
                description=description,
                meta_title=meta_title,
                meta_description=meta_description,
                meta_keywords=meta_keywords,
                parent_id=parent,
                image=image,
                top=top,
                column=column,
                sort_order=sort_order,
                status=status,
                slug=slug,
            )
            cat.save()
            return redirect('admin_category')
        else:
            return render(request, 'shop/category/category_add.html', {'form': form_new})
    context = {
        'form': CategoryForm(),
        'categorys': Category.objects.filter(parent=None)
    }
    return render(request, 'shop/category/category_add.html', context)


# Удаление категорий
@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()
    return redirect('admin_category')


# Редкатирование категорий
@user_passes_test(lambda u: u.is_superuser)
def category_edit(request, pk):
    cat = Category.objects.get(id=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=cat)
        if form.is_valid():
            form.save()
            return redirect('admin_category')
        else:
            return render(request, 'shop/category/category_edit.html', {'form': form})


    
    context = {
        'form': CategoryForm(instance=cat),
        'category': cat,
        'categorys': Category.objects.filter(parent=None).exclude(id=pk)
    }

    return render(request, 'shop/category/category_edit.html', context)

from django.core.paginator import Paginator

# Производители
@user_passes_test(lambda u: u.is_superuser)
def admin_manufacturer(request):
    q = request.GET.get('q')
    sort = request.GET.getlist('sort')
    try:
        sort_t = sort[0]
    except:
        sort_t = sort
    try:
        manufacturer = Manufacturer.objects.filter(Q(name__icontains=q)).order_by(*sort)
    except:
        manufacturer = Manufacturer.objects.all().order_by(*sort)

    paginator = Paginator(manufacturer, 50) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        # Разрешить поиск на странице
        'search': 'search',
        'page_obj': page_obj,
        'q': q,
        'sort': sort_t,
    }
    return render(request, 'shop/manufacturer/manufacturer.html', context)

# Добавить производителя
@user_passes_test(lambda u: u.is_superuser)
def manufacturer_add(request):
    if request.method == 'POST':
        form_new = ManufacturerForm(request.POST, request.FILES)
        if form_new.is_valid():
            form_new.save()
            return redirect('admin_manufacturer')
        else:
            return render(request, 'shop/manufacturer/manufacturer_add.html', {'form': form_new})
    form = ManufacturerForm()
    context = {
       'form': form,
    }
    return render(request, 'shop/manufacturer/manufacturer_add.html', context)


# Редактировать производителя
# !!! Некорректное поведение при редкатирвовании картинки, поправить !!!
@user_passes_test(lambda u: u.is_superuser)
def manufacturer_edit(request, pk):
    manufacturer = Manufacturer.objects.get(id=pk)
    if request.method == 'POST':
        form_new = ManufacturerForm(request.POST, request.FILES, instance=manufacturer)
        if form_new.is_valid():
            form_new.save()
            return redirect('admin_manufacturer')
        else:
            return render(request, 'shop/manufacturer/manufacturer_edit.html', {'form': form_new})
    
    form = ManufacturerForm(instance=manufacturer)
    context = {
       'form': form,
    }
    return render(request, 'shop/manufacturer/manufacturer_edit.html', context)


# Удалить производителя
@user_passes_test(lambda u: u.is_superuser)
def manufacturer_delete(request, pk):
    manufacturer = Manufacturer.objects.get(id=pk)
    manufacturer.delete()
    return redirect('admin_manufacturer')



# Опции
@user_passes_test(lambda u: u.is_superuser)
def admin_option_type(request):
    q = request.GET.get('q')
    sort = request.GET.getlist('sort')
    try:
        sort_t = sort[0]
    except:
        sort_t = sort
    try:
        options = OptionType.objects.filter(Q(name__icontains=q)).order_by(*sort)
    except:
        options = OptionType.objects.all().order_by(*sort)
    context = {
        # Разрешить поиск на странице
        'search': 'search',
        'options': options,
        'q': q,
        'sort': sort_t,
    }
    return render(request, 'shop/option_type/option_type.html', context)


# Добавить опцию
@user_passes_test(lambda u: u.is_superuser)
def option_type_add(request):
    if request.method == 'POST':
        form_new = OptionTypeForm(request.POST)
        if form_new.is_valid():
            form_new.save()
            return redirect('admin_option_type')
        else:
            return render(request, 'shop/option_type/option_type_add.html', {'form': form_new})
    form = OptionTypeForm()
    context = {
       'form': form,
    }
    return render(request, 'shop/option_type/option_type_add.html', context)

# Редкатировать опцию
@user_passes_test(lambda u: u.is_superuser)
def option_type_edit(request, pk):
    option_type = OptionType.objects.get(id=pk)
    if request.method == 'POST':
        form_new = OptionTypeForm(request.POST, instance=option_type)
        if form_new.is_valid():
            form_new.save()
            return redirect('admin_option_type')
        else:
            return render(request, 'shop/option_type/option_type_edit.html', {'form': form_new})
    
    form = OptionTypeForm(instance=option_type)
    context = {
       'form': form,
    }
    return render(request, 'shop/option_type/option_type_edit.html', context)

# Удалить опцию
@user_passes_test(lambda u: u.is_superuser)
def option_type_delete(request, pk):
    option_type = OptionType.objects.get(id=pk)
    option_type.delete()
    return redirect('admin_option_type')


# Характеристики
@user_passes_test(lambda u: u.is_superuser)
def admin_char(request):
    context = {
        'groups': CharGroup.objects.all(),
        'chars': CharName.objects.filter(group=None)
    }
    return render(request, 'shop/char/char.html', context)

@user_passes_test(lambda u: u.is_superuser)
def char_group_add(request):
    if request.method == 'POST':
        form_new = CharGroupForm(request.POST)
        if form_new.is_valid():
            form_new.save()
            return redirect('admin_char')
        else:
            return render(request, 'shop/char/char_group_add.html', {'form': form})

    form = CharGroupForm()
    context = {
        'form': form,
    }
    return render(request, 'shop/char/char_group_add.html', context)

@user_passes_test(lambda u: u.is_superuser)
def char_group_edit(request, pk):
    char_group = CharGroup.objects.get(id=pk)
    if request.method == 'POST':
        form_new = CharGroupForm(request.POST, instance=char_group)
        if form_new.is_valid():
            form_new.save()
            return redirect('admin_char')
        else:
            return render(request, 'shop/char/char_group_edit.html', {'form': form})
    form = CharGroupForm(instance=char_group)
    context = {
        'form': form,
    }
    return render(request, 'shop/char/char_group_edit.html', context)

@user_passes_test(lambda u: u.is_superuser)
def char_group_delete(request, pk):
    char_group = CharGroup.objects.get(id=pk)
    char_group.delete()
    return redirect('admin_char')

@user_passes_test(lambda u: u.is_superuser)
def char_add(request):
    if request.method == 'POST':
        form_new = CharNameForm(request.POST)
        if form_new.is_valid():
            form_new.save()
            return redirect('admin_char')
        else:
            return render(request, 'shop/char/char_add.html', {'form': form})

    form = CharNameForm()
    context = {
        'form': form,
    }
    return render(request, 'shop/char/char_add.html', context)

@user_passes_test(lambda u: u.is_superuser)
def char_edit(request, pk):
    char = CharName.objects.get(id=pk)
    if request.method == 'POST':
        form_new = CharNameForm(request.POST, instance=char)
        if form_new.is_valid():
            form_new.save()
            return redirect('admin_char')
        else:
            return render(request, 'shop/char/char_edit.html', {'form': form})

    form = CharNameForm(instance=char)
    context = {
        'form': form,
    }
    return render(request, 'shop/char/char_edit.html', context)

@user_passes_test(lambda u: u.is_superuser)
def char_delete(request, pk):
    char = CharName.objects.get(id=pk)
    char.delete()
    return redirect('admin_char')


# Товары
@user_passes_test(lambda u: u.is_superuser)
def admin_product(request):
    q = request.GET.get('q')
    sort = request.GET.getlist('sort')
    try:
        sort_t = sort[0]
    except:
        sort_t = sort
    try:
        product = Product.objects.filter(Q(name__icontains=q)).order_by(*sort)
    except:
        product = Product.objects.all().order_by(*sort)


    paginator = Paginator(product, 50) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        # Разрешить поиск на странице
        'search': 'search',
        'page_obj': page_obj,
        'q': q,
        'sort': sort_t,
    }


    return render(request, 'shop/product/product.html', context)



# Добавить товар
@user_passes_test(lambda u: u.is_superuser)
def product_add(request):
    form = ProductForm()    
    option_form = ProductOptionForm()
    product_char_form = ProductCharForm()
    image_form = ProductImageForm()
    if request.method == 'POST':
        form_new = ProductForm(request.POST, request.FILES)
        if form_new.is_valid():
            form_new.save()
            product = Product.objects.get(slug=request.POST['slug'])

            # Изображения

            images = request.FILES.getlist('src')
            
            for image in images:
                img = ProductImage(parent=product, src=image)
                img.save()

            # Опции

            # opt = ProductOption(
            #     parent = product,
            #     option_sku=product.sku,
            #     option_value = product.name,
            #     option_stock = product.stock,
            #     option_price = 0,
            #     option_subtract = product.subtract,
            #     image_status = False,

            # )
            # opt.save()

            
            options = request.POST.getlist('type')
            option_sku = request.POST.getlist('option_sku')
            option_value = request.POST.getlist('option_value')
            option_stock = request.POST.getlist('option_stock')
            option_price = request.POST.getlist('option_price')
            option_subtract = request.POST.getlist('option_subtract')
            image_status = request.POST.getlist('image_status')
            o_count = 0
            for option in options:
                opt = ProductOption(
                    parent = product,
                    type_id = option,
                    option_sku = option_sku[o_count],
                    option_value = option_value[o_count],
                    option_stock = option_stock[o_count],
                    option_price = option_price[o_count],
                    option_subtract = option_subtract[o_count],
                    image_status = image_status[o_count],
                )
                opt.save()
                
                try:
                    images_name = 'option_images-'+str(o_count)
                    option_images = request.FILES.getlist(images_name)
                    for image in option_images:
                        o_image = OptionImage(parent=opt, src=image)
                        o_image.save()
                except:
                    pass

                o_count += 1

            # Характеристики

            char_name = request.POST.getlist('text_name')
            char_value = request.POST.getlist('char_value')
            char_count = 0

            for char in char_name:

                value = char_value[char_count]
                product_char = ProductChar(
                    char_name_id = char,
                    parent = product,
                    char_value = value
                )
                product_char.save()
                char_count += 1


            product.save()

            return redirect('admin_product')
        else:
            return render(request, 'shop/product/product_add.html', {
                'form': form_new,
                'option_form': option_form,
                'product_char_form': product_char_form,
                'image_form': image_form,
                })

    context = {
       'form': form,
       'option_form': option_form,
       'product_char_form': product_char_form,
       'image_form': image_form,

    }
    return render(request, 'shop/product/product_add.html', context)

@user_passes_test(lambda u: u.is_superuser)
def product_edit(request, pk):

    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product) 
    option_form = ProductOptionForm()
    product_char_form = ProductCharForm()

    options = ProductOption.objects.filter(parent_id=pk)
    # chars = ProductChar.objects.filter(parent_id=pk)
    images = ProductImage.objects.filter(parent_id=pk)
    all_options = OptionType.objects.all()
    all_chars = CharName.objects.all()
    

    form_new = ProductForm(request.POST, request.FILES, instance=product) 
    if request.method == 'POST':  
        if form_new.is_valid():
            form_new.save()

            # Изображения

            images = request.FILES.getlist('src')
            
            for image in images:
                img = ProductImage(parent=product, src=image)
                img.save()


            # Характеристики 
            char_name = request.POST.getlist('text_name')
            char_value = request.POST.getlist('char_value')
            char_count = 0

            for char in char_name:

                value = char_value[char_count]
                product_char = ProductChar(
                    char_name_id = char,
                    parent = product,
                    char_value = value
                )
                product_char.save()
                char_count += 1

            old_char_id = request.POST.getlist('old_char_id')
            old_char_name = request.POST.getlist('old_text_name')
            old_char_value = request.POST.getlist('old_char_value')
            old_char_count = 0

            for id in old_char_id:

                old_char = ProductChar.objects.get(id=id)
                old_char.char_name_id = old_char_name[old_char_count]
                old_char.char_value = old_char_value[old_char_count]
                
                old_char.save()
                old_char_count += 1
            
            
            
        
            # Изменение старых опций
            old_id = request.POST.getlist('old_id')
            old_type = request.POST.getlist('old_type')
            old_option_value = request.POST.getlist('old_option_value')
            old_option_sku = request.POST.getlist('old_option_sku')
            old_option_stock = request.POST.getlist('old_option_stock')
            old_option_price = request.POST.getlist('old_option_price')
            old_option_subtract = request.POST.getlist('old_option_subtract')
            old_image_status = request.POST.getlist('old_image_status')
            old_count = 0
            for old in old_id:
                price = old_option_price[old_count]
                price = price.replace(',', '.')
                old_option = ProductOption.objects.get(id=old)
                old_option.type_id = old_type[old_count]
                old_option.option_sku = old_option_sku[old_count]
                old_option.option_value = old_option_value[old_count]
                old_option.option_stock = old_option_stock[old_count]
                old_option.option_price = price
                old_option.option_subtract = old_option_subtract[old_count]
                old_option.image_status = old_image_status[old_count]
                old_option.save()
                try:
                    old_images = request.FILES.getlist('option_images_old-'+str(old_count))
                    for im in old_images:
                        image = OptionImage(src=im, parent=old_option)
                        image.save()
                except Exception as e:
                    print(e)



                old_count += 1

            # Опции
            options = request.POST.getlist('type')
            option_sku = request.POST.getlist('option_sku')
            option_value = request.POST.getlist('option_value')
            option_stock = request.POST.getlist('option_stock')
            option_price = request.POST.getlist('option_price')
            option_subtract = request.POST.getlist('option_subtract')
            image_status = request.POST.getlist('image_status')
            o_count = 0
            for option in options:
                opt = ProductOption(
                    parent = product,
                    type_id = option,
                    option_sku = option_sku[o_count],
                    option_value = option_value[o_count],
                    option_stock = option_stock[o_count],
                    option_price = Decimal(option_price[o_count]),
                    option_subtract = option_subtract[o_count],
                    image_status = image_status[o_count],
                )
                opt.save()
                
                try:
                    images_name = 'option_images-'+str(o_count)
                    option_images = request.FILES.getlist(images_name)
                    for image in option_images:
                        o_image = OptionImage(parent=opt, src=image)
                        o_image.save()
                except:
                    pass

                o_count += 1

            return redirect('admin_product')
        else:
            return render(request, 'shop/product/product_edit.html', {'form': form})

    context = {
        'form': form,
        'option_form': option_form,
        'product_char_form': product_char_form,
        'options': options,
        'all_options': all_options,
        'all_chars': all_chars,
        # 'chars': chars,
        'images': images,
        'product': product
    }

    return render(request, 'shop/product/product_edit.html', context)
    

@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):

    product = Product.objects.get(id=pk)
    product.delete()


    return redirect('admin_product')

@user_passes_test(lambda u: u.is_superuser)
def product_image_delete(request, pk):

    image = ProductImage.objects.get(id=pk)
    image.delete()

    return redirect('admin_product')


@user_passes_test(lambda u: u.is_superuser)
def product_char_delete(request, pk):

    product_char = ProductChar.objects.get(id=pk)
    product_char.delete()

    return redirect('admin_product')

@user_passes_test(lambda u: u.is_superuser)
def option_delete(request, pk):
        
    option = ProductOption.objects.get(id=pk)
    option.delete()

    return redirect('admin_product')

@user_passes_test(lambda u: u.is_superuser)
def option_image_delete(request, pk):

    image = OptionImage.objects.get(id=pk)
    image.delete()

    parent_id = image.parent.id

    option = ProductOption.objects.get(id=parent_id)
    images = option.images.all()
    
    if images.count() == 0:
        option.image_status = False
        option.save()

    return redirect('admin_product')






# !!! БЛОГ !!!
@user_passes_test(lambda u: u.is_superuser)
def blog_settings(request):
    blog_settings = BlogSetup.objects.get()
    if request.method == 'POST':
        form = BlogSetupForm(request.POST, instance=blog_settings)
        if form.is_valid():
            form.save()
            return redirect('blog_settings')
        else:
            return render(request, 'blog/blog_settings.html', {'form':form})

    form = BlogSetupForm(instance=blog_settings)
    context = {
        'form': form
    }

    return render(request, 'blog/blog_settings.html', context)




@user_passes_test(lambda u: u.is_superuser)
def blog_category(request):
    q = request.GET.get('q')
    sort = request.GET.getlist('sort')
    try:
        sort_t = sort[0]
    except:
        sort_t = sort
    try:
        blog_category = BlogCategory.objects.filter(Q(name__icontains=q)).order_by(*sort)
    except:
        blog_category = BlogCategory.objects.all().order_by(*sort)
    context = {
        # Разрешить поиск на странице
        'search': 'search',
        'blog_category': blog_category,
        'q': q,
        'sort': sort_t,
    }
    return render(request, 'blog/blog_category/blog_category.html', context)


@user_passes_test(lambda u: u.is_superuser)
def blog_category_add(request):
    if request.method == 'POST':
        form = BlogCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog_category')
        else:
            return render(request, 'blog/blog_category/blog_category_add.html', {'form': form})
    form = BlogCategoryForm()
    context = {
        'form':form,
    } 
    return render(request, 'blog/blog_category/blog_category_add.html', context)

@user_passes_test(lambda u: u.is_superuser)
def blog_category_edit(request, pk):
    blog_category = BlogCategory.objects.get(id=pk)
    if request.method == 'POST':
        form = BlogCategoryForm(request.POST, request.FILES, instance=blog_category)
        if form.is_valid():
            form.save()
            return redirect('blog_category')
        else:
            return render(request, 'blog/blog_category/blog_category_edit.html', {'form': form})
    form = BlogCategoryForm(instance=blog_category)
    context = {
        'form':form,
    } 
    return render(request, 'blog/blog_category/blog_category_edit.html', context)

@user_passes_test(lambda u: u.is_superuser)
def blog_category_delete(request, pk):
    blog_category = BlogCategory.objects.get(id=pk)
    blog_category.delete()
    return redirect('blog_category')


@user_passes_test(lambda u: u.is_superuser)
def blog_post(request):
    q = request.GET.get('q')
    sort = request.GET.getlist('sort')
    try:
        sort_t = sort[0]
    except:
        sort_t = sort
    try:
        posts = Post.objects.filter(Q(name__icontains=q)).order_by(*sort)
    except:
        posts = Post.objects.all().order_by(*sort).order_by('-id')
        # posts.delete()


    context = {
        # Разрешить поиск на странице
        'search': 'search',
        'posts': posts,
        'q': q,
        'sort': sort_t,
    }


    return render(request, 'blog/blog_post/blog_post.html', context)


@user_passes_test(lambda u: u.is_superuser)
def post_add(request):
    try:
        post = Post.objects.get(draft=True)
    except:
        post = Post(draft=True)
        post.save()

    form = PostForm(instance=post)
    block_form = PostBlockForm()
    if request.method == 'POST':
        post.draft = False
        post.published = True
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()

            return redirect('blog_post')
    context = {
        'post': post,
        'form': form,
        'block_form': block_form,
    }


    return render(request, 'blog/blog_post/post_add.html', context)

@user_passes_test(lambda u: u.is_superuser)
def post_edit(request, pk):
    
    post = Post.objects.get(id=pk)
    
    form = PostForm(instance=post)
    block_form = PostBlockForm()
    if request.method == 'POST':
        post.draft = False
        post.published = True
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()

            return redirect('blog_post')
    context = {
        'post': post,
        'form': form,
        'block_form': block_form,
    }


    return render(request, 'blog/blog_post/post_edit.html', context)

@user_passes_test(lambda u: u.is_superuser)
def post_delete(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('blog_post')


@user_passes_test(lambda u: u.is_superuser)
def post_draft(request):

    if request.method == 'POST':
        post = Post.objects.get(draft=True)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save() 

            return redirect('blog_post')

        else:

            return render(request, 'blog/blog_post/post_add.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def post_block(request):
    if request.method == 'POST':
        parent = request.POST['parent']
        type = request.POST['type']
        order = request.POST['order']
        next = request.POST['next']
        try:
            text = request.POST['text']
            block = PostBlock(parent_id=parent, text=text, type=type, order=order)
            block.save()
        except:
            pass
        try:
            title = request.POST['title']
            block = PostBlock(parent_id=parent, title=title, type=type, order=order)
            block.save()
        except:
            pass
        try:
            image = request.FILES['image']
            block = PostBlock(parent_id=parent, image=image, type=type, order=order)
            block.save()
        except:
            pass
        try:
            video = request.FILES['video']
            block = PostBlock(parent_id=parent, video=video, type=type, order=order)
            block.save()
        except:
            pass

        
        return redirect(next)


@user_passes_test(lambda u: u.is_superuser)
def post_block_edit(request, pk):
    block = PostBlock.objects.get(id=pk)
    next = request.POST['next']
    if request.method == 'POST':
        try:
            text = request.POST['text']
            block.text = text
            block.save()
        except:
            pass
        try:
            title = request.POST['title']
            block.title = title
            block.save()
        except:
            pass
        try:
            image = request.FILES['image']
            block.image = image
            block.save()
        except:
            pass
        try:
            video = request.FILES['video']
            block.video = video
            block.save()
        except:
            pass

        
        return redirect(next)


@user_passes_test(lambda u: u.is_superuser)
def post_block_edit_delete(request, pk):

    block = PostBlock.objects.get(id=pk)
    block.delete()

    return redirect('post_edit', block.parent.id)


@user_passes_test(lambda u: u.is_superuser)
def post_block_add_delete(request, pk):

    block = PostBlock.objects.get(id=pk)
    block.delete()

    return redirect('post_add')



# !!! СТАТИКА !!!


@user_passes_test(lambda u: u.is_superuser)
def admin_slider(request):
    sliders = Slider.objects.all()
    try:
        slider_setup = SliderSetup.objects.get()
    except:
        slider_setup = SliderSetup()
        slider_setup.save()

    if request.method == 'POST':
        form = SliderSetupForm(request.POST, instance=slider_setup)
        if form.is_valid():
            form.save()
            return redirect('admin_slider')
        else:
            return render(request, 'static/slider.html', {'form': form})

    setup_form = SliderSetupForm(instance=slider_setup)
    context = {
        'setup_form': setup_form,
        'sliders': sliders
    }
    return render(request, 'static/slider.html', context)

@user_passes_test(lambda u: u.is_superuser)
def slider_add(request):

    if request.method == 'POST':
        form = SliderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_slider')

        else:
            return render(request, 'static/slider_add.html', {'form': form})
    form = SliderForm()
    context = {
        'form': form,
    }

    return render(request, 'static/slider_add.html', context)



@user_passes_test(lambda u: u.is_superuser)
def slider_edit(request, pk):
    slider = Slider.objects.get(id=pk)
    if request.method == 'POST':
        form = SliderForm(request.POST, request.FILES, instance=slider)
        if form.is_valid():
            form.save()
            return redirect('admin_slider')

        else:
            return render(request, 'static/slider_edit.html', {'form': form})
    form = SliderForm(instance=slider)
    context = {
        'form': form,
    }

    return render(request, 'static/slider_edit.html', context)


@user_passes_test(lambda u: u.is_superuser)
def slider_delete(request, pk):
    slider = Slider.objects.get(id=pk)
    slider.delete()
    return redirect('admin_slider')


@user_passes_test(lambda u: u.is_superuser)
def admin_pages(request):

    context = {
        'pages': Page.objects.all()
    }

    return render(request, 'static/admin_pages.html', context)


@user_passes_test(lambda u: u.is_superuser)
def page_add(request):

    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_pages')

        else:
            return render(request, 'static/page_add.html', {'form': form})

    form = PageForm()
    context = {
        'form': form,
    }

    return render(request, 'static/page_add.html', context)

@user_passes_test(lambda u: u.is_superuser)
def page_edit(request, pk):
    page = Page.objects.get(id=pk)
    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            form.save()
            return redirect('admin_pages')
        else:
            return render(request, 'static/page_edit.html', {'form': form})
            
    form = PageForm(instance=page)
    context = {
        'form': form,
    }
    return render(request, 'static/page_edit.html', context)

# !!! СТАТИКА !!!


# !!! Пользователи USERS !!!


@user_passes_test(lambda u: u.is_superuser)
def admin_users(request):

    users = UserProfile.objects.filter()

    context = {
        'users': users
    }

    return render(request, 'users/admin_users.html', context)

@user_passes_test(lambda u: u.is_superuser)
def users_delete(request, pk):

    user = UserProfile.objects.get(id=pk)
    user.delete()

    return redirect('admin_users')


# !!! Пользователи USERS !!!






# !!! Услуги SERV


@user_passes_test(lambda u: u.is_superuser)
def setup_serv(request):

    try:
        serv_setup = ServSetup.objects.get()
        form = ServSetupForm(instance=serv_setup)
    except:
        serv_setup = ServSetup.objects.create()
        form = ServSetupForm()


    if request.method == 'POST':
        form = ServSetupForm(request.POST, request.FILES, instance=serv_setup)
        if form.is_valid():
            form.save()
            return redirect('setup_serv')
        else:

            return render(request, 'serv/serv_settings.html', {'form': form})


   

    context = {
        'form': form
    }

    return render(request, 'serv/serv_settings.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_serv(request):

    context = {
        'servs': Service.objects.all()
    }

    return render(request, 'serv/admin_serv.html', context)
@user_passes_test(lambda u: u.is_superuser)
def serv_add(request):

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_serv')

        else:
            return render(request, 'serv/serv_add.html', {'form':form})


    form = ServiceForm()
    context = {
        'form': form
    }

    return render(request, 'serv/serv_add.html', context)

@user_passes_test(lambda u: u.is_superuser)
def serv_edit(request, pk):
    serv = Service.objects.get(id=pk)

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=serv)
        if form.is_valid():
            form.save()
            return redirect('admin_serv')

        else:
            return render(request, 'serv/serv_edit.html', {'form':form})


    form = ServiceForm(instance=serv)
    context = {
        'form': form
    }

    return render(request, 'serv/serv_edit.html', context)

@user_passes_test(lambda u: u.is_superuser)
def serv_delete(request, pk):

    serv = Service.objects.get(id=pk)
    serv.delete()

    return redirect('admin_serv')

# !!! Услуги SERV



# !!!
@user_passes_test(lambda u: u.is_superuser)
def setup_api(request):

    if request.method == 'POST':
        form = DiapasoneForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('setup_api')
        else:

            return render(request, 'shop/setup_api.html', {'form': form})



    diapasones = Diapasone.objects.all().order_by('start')

    form = DiapasoneForm()
    context = {
        'form': form,
        'diapasones': diapasones
    }

    return render(request, 'shop/setup_api.html', context)


@user_passes_test(lambda u: u.is_superuser)
def remove_api(request, pk):
    diapasone = Diapasone.objects.get(id=pk)
    diapasone.delete()


    return redirect('setup_api')




def admin_gallery(request):
    images = GalleryImage.objects.all()
    context = {
        'images': images
        
    }
    return render(request, 'static/admin_gallery.html', context)


def gallery_add(request):

    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_gallery')

        else:
            return render(request, 'static/gallery_add.html', {'form': form})

    form = GalleryImageForm()
    context = {
        'form': form
    }

    return render(request, 'static/gallery_add.html', context)


def gallery_edit(request, pk):
    image = GalleryImage.objects.get(id=pk)

    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            return redirect('admin_gallery')

        else:
            return render(request, 'static/gallery_edit.html', {'form': form})

    form = GalleryImageForm(instance=image)
    context = {
        'form': form
    }

    return render(request, 'static/gallery_edit.html', context)


def gallery_delete(request, pk):
    image = GalleryImage.objects.get(id=pk)
    image.delete()

    return redirect('admin_gallery')







def admin_reviews(request):
    admin_reviews = Reviews.objects.all()
    context = {
        'admin_reviews': admin_reviews
        
    }
    return render(request, 'pages/reviews/admin_reviews.html', context)


def reviews_add(request):

    if request.method == 'POST':
        form = ReviewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_reviews')

        else:
            return render(request, 'pages/reviews/reviews_add.html', {'form': form})

    form = ReviewsForm()
    context = {
        'form': form
    }

    return render(request, 'pages/reviews/reviews_add.html', context)


def reviews_edit(request, pk):
    review = Reviews.objects.get(id=pk)

    if request.method == 'POST':
        form = ReviewsForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect('admin_reviews')

        else:
            return render(request, 'pages/reviews/reviews_edit.html', {'form': form})

    form = ReviewsForm(instance=review)
    context = {
        'form': form
    }

    return render(request, 'pages/reviews/reviews_edit.html', context)


def reviews_delete(request, pk):
    review = Reviews.objects.get(id=pk)
    review.delete()

    return redirect('admin_reviews')