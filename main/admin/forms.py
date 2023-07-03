from django import forms
from coupons.models import Coupon
from orders.models import Order 
from setup.models import BaseSettings, Colors, RecaptchaSettings, EmailSettings, ThemeSettings
from shop.models import Category, Product, Manufacturer, OptionType, CharGroup, CharName, ProductChar, ProductOption, ProductImage, ShopSetup
from blog.models import BlogCategory, BlogSetup, Post, PostBlock
from home.models import Reviews, SliderSetup, Slider, Page, GalleryImage
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from serv.models import Service, ServiceGroup, ServiceItem, ServSetup
from pay.models import PaymentSet, Tinkoff, Yookassa, AlfaBank, PayKeeper
from api.models import Diapasone




class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Имя'
            }),
            'date': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Дата'
            }),
            'text': forms.Textarea(attrs={
                'class': 'input',
                'placeholder': 'Описание'
            }),
          
        }







class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Название'
            }),
            'description': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Описание'
            }),
          
        }



# Наценка на поставщиков


class DiapasoneForm(forms.ModelForm):
    class Meta:
        model = Diapasone
        fields = '__all__'
        widgets = {
            'start': forms.NumberInput(attrs={
                'class': 'input',
            }),
            'end': forms.NumberInput(attrs={
                'class': 'input',
            }),
            
           
            'persent': forms.NumberInput(attrs={
                'class': 'input',
            }),
        }



# Платежи


class YookassaForm(forms.ModelForm):
    class Meta:
        model = Yookassa
        fields = '__all__'
        
        widgets = {
            'shop_id': forms.TextInput(attrs={
                'class': 'input',
            }),
            'key': forms.TextInput(attrs={
                'class': 'input',
            }),
            
           
            'vat_code': forms.Select(attrs={
                'class': 'input',
            }),
        }

class AlfaBankForm(forms.ModelForm):
    class Meta:
        model = AlfaBank
        fields = '__all__'
        
        widgets = {
            'login': forms.TextInput(attrs={
                'class': 'input',
            }),
            'password': forms.TextInput(attrs={
                'class': 'input',
            }),
            'token': forms.TextInput(attrs={
                'class': 'input',
            })
        }



class PayKeeperForm(forms.ModelForm):
    class Meta:
        model = PayKeeper
        fields = '__all__'
        
        widgets = {
            'login': forms.TextInput(attrs={
                'class': 'input',
            }),
            'password': forms.TextInput(attrs={
                'class': 'input',
            }),
            'server': forms.TextInput(attrs={
                'class': 'input',
            })
        }


class TinkoffForm(forms.ModelForm):
    class Meta:
        model = Tinkoff
        fields = '__all__'
        
        widgets = {
            'terminalkey': forms.TextInput(attrs={
                'class': 'input',
            }),
            'password': forms.TextInput(attrs={
                'class': 'input',
            }),
            'taxation': forms.Select(attrs={
                'class': 'input',
            })
        }



class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentSet
        fields = '__all__'
        
        widgets = {
           
            'name': forms.Select(attrs={
                'class': 'input',
            }),
        }


















# Услуги

class ServiceForm(forms.ModelForm):
    text = forms.CharField(label='Текст страницы', required=False, widget=CKEditorUploadingWidget())
    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
           
            'name': forms.TextInput(attrs={
                'class': 'input',
            }),
            'meta_h1': forms.TextInput(attrs={
                'class': 'input',
            }),
           
            'meta_title': forms.TextInput(attrs={
                'class': 'input',
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'input',
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'input',
            }),
            'min_srok': forms.TextInput(attrs={
                'class': 'input',
            }),
            'how': forms.TextInput(attrs={
                'class': 'input',
            }),
            'slug': forms.TextInput(attrs={
                'class': 'input',
            }),
            'price': forms.TextInput(attrs={
                'class': 'input',
            }),
        }




class ServSetupForm(forms.ModelForm):

    description = forms.CharField(label='Текст описания страницы', required=False, widget=CKEditorUploadingWidget())
    class Meta:
        model = ServSetup
        fields = '__all__'

        widgets = {
           
            'meta_h1': forms.TextInput(attrs={
                'class': 'input',
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'input',
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'input',
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'input',
            }),
        }


# Статус заказа
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'status'
        ]
        widgets = {
           
            'status': forms.Select(attrs={
                'class': 'input',
            }),
        }

# Страницы 
class PageForm(forms.ModelForm):
    text = forms.CharField(label='Текст страницы', required=False, widget=CKEditorUploadingWidget())
    class Meta:
        model = Page
        fields = "__all__"
        
        widgets = {
           
            'type': forms.Select(attrs={
                'class': 'input',
            }),
            'name': forms.TextInput(attrs={
                'class': 'input',
            }),
            'meta_h1': forms.TextInput(attrs={
                'class': 'input',
            }),
           
            'meta_title': forms.TextInput(attrs={
                'class': 'input',
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'input',
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'input',
            }),
        }



# Cлайдер

class SliderSetupForm(forms.ModelForm):
    
    class Meta:
        model = SliderSetup
        fields = "__all__"
        widgets = {
            'speed': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            })
        }



class SliderForm(forms.ModelForm):
    
    class Meta:
        model = Slider
        fields = [
            'name',
            'title',
            'text',
            'link',
            'image'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Название',
            }),
            'title': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Заголовок (не обязательно)',
            }),
            'text': forms.Textarea(attrs={
                'class': 'input',
                'placeholder': 'Текст (не обязательно)',
            }),
            'button_text': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Текст кнопки (не обязательно)',
            }),
            'link': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ссылка (не обязательно)',
            }),
        }



# Блог

class BlogSetupForm(forms.ModelForm):
    description = forms.CharField(label='Описание страницы', required=False, widget=CKEditorUploadingWidget())
    class Meta:
        model = BlogSetup
        fields = "__all__"
        widgets = {
            'meta_h1': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'h1',
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Мета заголовок',
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'input',
                'placeholder': 'Мета описание',
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ключевые слова',
            }),
        }


class PostBlockForm(forms.ModelForm):
    # text = forms.CharField(label='Текст', required=False, widget=CKEditorUploadingWidget())
    class Meta:
        model = PostBlock
        fields = [
            'parent',
            'type',
            'text',
            'title',
            'image',
            'video',
            'order',

        ]
        labels = {
            'title': 'Заголовок',
          
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input submit',
                'placeholder': 'Заголовок',
            }),
            'text': forms.Textarea(attrs={
                'class': 'input submit',
                'placeholder': 'Текст',
            }),
            'video': forms.FileInput(attrs={
                'class': 'submit-file',
                'accept': 'video/*'
            
            }),
            'image': forms.FileInput(attrs={
                'class': 'submit-file',
                'accept': 'image/*'
                
            }),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'parent',
            'name',
          
            'meta_h1',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'image',
            'slug',
        ]   
        labels = {
            'parent': '',
            'name': 'Название',
            
            'meta_h1': 'Заголовок h1',
            'meta_title': 'Мета тайтл',
            'meta_description': 'Мета описание',
            'meta_keywords': 'Ключевые слова',
            'image': 'Изображение',
            'slug': 'SEO URL',
        }
        widgets = {
            'parent': forms.Select(attrs={
                'class': 'hidden',
                'placeholder': 'Категория',
                'hidden': 'hidden'
            }),
            
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Название',
            }),
            'meta_h1': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Заголовок h1',
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Мета тайтл',
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'input',
                'placeholder': 'Мета описание',
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ключевые слова',
            }),
            
            'slug': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'SEO URL',
            }),
        }

class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogCategory

        fields = [
            'name',
            'meta_h1',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'image',
            'slug',

        ]        
        labels = {
            'name': 'Название',
            'meta_h1': 'Заголовок h1',
            'meta_title': 'Мета тайтл',
            'meta_description': 'Мета описание',
            'meta_keywords': 'Ключевые слова',
            'image': 'Изображение',
            'slug': 'SEO URL',
        }
        widgets = {
          
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Название',
            }),
            'meta_h1': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Заголовок h1',
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Мета тайтл',
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'input',
                'placeholder': 'Мета описание',
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ключевые слова',
            }),
            'slug': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'SEO URL',
            }),
        }



# Настройки магазина

class ShopSetupForm(forms.ModelForm):
    description = forms.CharField(label='Описание каталога', required=False, widget=CKEditorUploadingWidget())
    class Meta:
        model = ShopSetup
        fields = "__all__"
        widgets = {
            'status': forms.Select(attrs={
                'class': 'input',
                'placeholder': '',
            }),
            'meta_h1': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
        }


# Маркетинг
class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = "__all__"
        labels = {
            'code': 'Код купона',
            'valid_from': 'Дата начала акции',
            'valid_to': 'Дата окончания акции',
            'discount': 'Скидка',
            'active': 'Активность',
        }
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Код купона',
            }),
            'valid_from': forms.DateInput(attrs={
                'class': 'input',
                'type': 'date',
                
            }),
            'valid_to': forms.DateInput(attrs={
                'class': 'input',
                'type': 'date',
                
            }),

            
            'discount': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Скидка',
            }),
           
            
        }


# Товар и опции товара
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage

        fields = [
            'parent',
            'src'
        ]
        labels = {
            'src': 'Выбрать изображение'
        }
        

class ProductOptionForm(forms.ModelForm):
    class Meta:
        model = ProductOption
        fields = [
            'type',
            'parent',
            'option_sku',
            'option_value',
            'option_stock',
            'option_price',
            'option_subtract',
            'image_status',
            
        ]
        labels = {
            'type': 'Тип опции',
            # 'parent': 'Продукт',
            'option_sku': 'Артикул',
            'option_value': 'Значение',
            'option_stock': 'Количество',
            'option_price': 'Добавить стоимость',
            'option_subtract': 'Вычитать со склада',
            'image_status': 'Включить изображения',
           
        }
        widgets = {
            'type': forms.Select(attrs={
                'class': 'input',
                'placeholder': 'Тип опции',
            }),
            'option_value': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
            }),
            'option_sku': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Артикул',
            }),
            'option_stock': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Количество',
            }),
            'option_price': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Добавить стоимость',
            }),
            # 'option_subtract': forms.CheckboxInput(attrs={
            #     'class': 'input',
                
            # }),
        }


class ProductCharForm(forms.ModelForm):
    class Meta:
        model = ProductChar
        fields = [
            'char_name',
            
            'char_value',
        ]
        labels = {
            'char_name': 'Название характеристики',
            
            'char_value': 'Значение',
        }
        widgets = {
            'char_name': forms.Select(attrs={
                'class': 'input',
                'placeholder': 'Название характеристики',
                'id': 'id_char_name',
               
            }),
            'char_value': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
                'id': 'id_char_value'
            }),
        }

class CharGroupForm(forms.ModelForm):
    class Meta:
        model = CharGroup
        fields = [
            'name',
            
        ]
        labels = {
            'name': 'Название группы характеристик',
           
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Название группы характеристик',
            }),
        }


class CharNameForm(forms.ModelForm):
    class Meta:
        model = CharName
        fields = [
            'group',
            'text_name',
            
        ]
        labels = {
            'group': 'Группа опций',
            'text_name': 'Название опции',
           
        }
        widgets = {
            'group': forms.Select(attrs={
                'class': 'input',
                'placeholder': 'Группа опций',
            }),
            'text_name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Название опции',
                'id': 'char_name'
            }),
        }


class OptionTypeForm(forms.ModelForm):
    class Meta:
        model = OptionType
        fields = [
            'name',
            'option_class',   
        ]
        labels = {
            'name': 'Название опции',
            'option_class': 'Тип опции',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Название опции',
            }),
            'option_class': forms.Select(attrs={
                'class': 'input',
                'placeholder': 'Тип опции',
            }),
        
        }



class ManufacturerForm(forms.ModelForm):
    description = forms.CharField(label='Описание производителя', required=False, widget=CKEditorUploadingWidget())
    class Meta:
        model = Manufacturer
        fields = [
            'name',
            'description',
            'meta_h1',
            'meta_title',
            'meta_description',
            'meta_keywords',
            
            'image',
            'sort_order',
        ]
        labels = {
            'name': 'Название производителя',
            'meta_h1': 'Заголовок h1',
            'meta_title': 'Мета заголовок',
            'meta_description': 'Мета описание',
            'meta_keywords': 'Ключевые слова',
            
            'image': 'Изображение',
            'sort_order': 'Порядок сортировки',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Название производителя',
            }),
            'meta_h1': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Заголовок h1',
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Мета заголовок',
            }),
            'meta_description': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Мета описание',
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ключевые слова',
            }),
           
            'sort_order': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Порядок сортировки',
            }),
        }


class ProductForm(forms.ModelForm):
    
    description = forms.CharField(label='Полное описание товара', required=False, widget=CKEditorUploadingWidget())
    
    class Meta:
        model = Product
        fields = [
            'name',
            'short_description',
            'description',
            'meta_h1',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'tags',
            
            'sku',
            'price',
            'old_price',
            'stock',
            'minimum',
            'subtract',
            'shipping',
            'top_collection',
            'new',
            'slug',
            
            'length',
            'width',
            'height',
           
            'length_class',
            'weight',
            'weight_class',
            'product_manufacturer',
            'parent',
            'product_connect',
            'thumb',
            'status',
            'sort_order',
        ]
        labels = {
            'name': 'Название товара',
            'short_description': 'Короткое описание товара',
            'meta_h1': 'Заголовок h1',
            'meta_title': 'Мета заголовок',
            'meta_description': 'Мета описание',
            'meta_keywords': 'Ключевые слова',
            'tags': 'Теги',
            'model': 'Модель',
            'sku': 'Артикул',
            'price': 'Цена (с учетом скидки)',
            'old_price': 'Старая цена',
            'stock': 'Количество',
            'minimum': 'Минимальное количество',
            'subtract': 'Вычитать со склада',
            'shipping': 'Необходима доставка',
            'top_collection': 'В коллекцию ТОП',
            'new': 'Новинка',
            'slug': 'SEO URL',
            
            'length': 'Длина',
            'width': 'Ширина',
            'height': 'Высота',
            
            'length_class': 'Единица измерения длины',
            'weight': 'Вес',
            'weight_class': 'Единица измерения веса',
            'product_manufacturer': 'Производитель',
            'parent': 'Категория',
            'product_connect': 'Связанные товары',
            'thumb': 'Изображение товара (превью)',
            'status': 'Статус',
            'sort_order': 'Порядок сортировки',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Название товара',
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'input',
                'placeholder': 'Короткое описание товара',
            }),
            'meta_h1': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'h1',
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Мета заголовок',
            }),
            'meta_description': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Мета описание',
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ключевые слова',
            }),
            'tags': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Теги',
            }),
            'model': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Модель',
            }),
            'sku': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Артикул',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Цена (с учетом скидки)',
            }),
            'old_price': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Старая цена',
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Количество',
            }),
            'minimum': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Минимальное количество для заказа',
            }),
            'slug': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'SEO URL',
            }),
            

            'length': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Длина',
            }),
            'width': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ширина',
            }),
            'height': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Высота',
            }),
            
            'length_class': forms.Select(attrs={
                'class': 'input',
                'placeholder': 'Единица измерения длины',
            }),
            'weight': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Вес',
            }),
            'weight_class': forms.Select(attrs={
                'class': 'input',
                'placeholder': 'Единица измерения веса',
            }),
            'product_manufacturer': forms.Select(attrs={
                'class': 'input',
                'placeholder': 'Производитель',
            }),
            'parent': forms.Select(attrs={
                'class': 'input',
                'placeholder': 'Категория',
            }),
            'product_connect': forms.SelectMultiple(attrs={
                'class': 'input',
                'placeholder': 'Связанные товары',
            }),
            
          
            # 'status': forms.Select(attrs={
            #     'class': 'input',
            #     'placeholder': 'Статус',
            # }),
            'sort_order': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Порядок сортировки',
            }),
        }


class CategoryForm(forms.ModelForm):
    description = forms.CharField(label='Описание категории', required=False, widget=CKEditorUploadingWidget())
    
    class Meta:
        model = Category
        fields = [
            # 'parent',
            'name',
            'description',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'image',
            'top',
            'column',
            'sort_order',
            'status',
            'slug',
            
        ]
        labels = {
            # 'parent': 'Родительская категория',

            'name': 'Название категории',
            'meta_title': 'Мета заголовок',
            'meta_description': 'Мета описание',
            'meta_keywords': 'Ключевые слова',
            
            'image': 'Изображение категории',
            'top': 'Отображать в меню',
            'column': 'Количество колонок',
            'sort_order': 'Порядок сортировки',
            'status': 'Активная',
            'slug': 'SEO URL',
            
            
        }
        widgets = {
           
            # 'parent': forms.Select(attrs={
            #     'class': 'input',
            #     'placeholder': 'Родительская категория',
            # }),
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Название категории',
            }),
           
            'meta_title': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Мета заголовок',
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Мета описание',
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ключевые слова',
            }),
            
            'top': forms.CheckboxInput(attrs={
                'class': '',
                'placeholder': 'Отображать в меню',
            }),
            'column': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Количество колонок',
            }),
            'sort_order': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Порядок сортировки',
            }),
            'status': forms.CheckboxInput(attrs={
                'class': '',
                'placeholder': 'Активная',
            }),
            'slug': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'SEO URL',
            }),
        }



class ThemeSettingsForm(forms.ModelForm):
    class Meta:
        model = ThemeSettings
        fields = [
            'name'
        ]
        widgets = {
            'name': forms.Select(attrs={
                'placeholder': 'Тема',
                'class': 'input'
            }),
        }
        labels = {
            'name': 'Выбрать тему',
        
        }

class ColorsForm(forms.ModelForm):
    class Meta:
        model = Colors
        fields = [
            'primary',
            'secondary',
            'success',
            'danger',
            'warning',
            'info',
        ]
        widgets = {
            'primary': forms.TextInput(attrs={
                
                'placeholder': 'Основной цвет',
                'type': 'color'
            }),
            'secondary': forms.TextInput(attrs={
                
                'placeholder': 'Дополнительный цвет',
                'type': 'color'
            }),
            'success': forms.TextInput(attrs={
                
                'placeholder': 'Цвет успеха',
                'type': 'color'
            }),
            'danger': forms.TextInput(attrs={
                
                'placeholder': 'Цвет ошибки',
                'type': 'color'
            }),
            'warning': forms.TextInput(attrs={
                
                'placeholder': 'Цвет предупреждения',
                'type': 'color'
            }),
            'info': forms.TextInput(attrs={
                
                'placeholder': 'Цвет инфо',
                'type': 'color'
            }),
        }
        labels = {
            'primary': 'Основной цвет',
            'secondary': 'Дополнительный цвет',
            'success': 'Цвет успеха',
            'danger': 'Цвет ошибки',
            'warning': 'Цвет предупреждения',
            'info': 'Цвет инфо',
        }

class RecaptchaSettingsForm(forms.ModelForm):
    class Meta:
        model = RecaptchaSettings
        fields = [
            'recaptcha_private_key',
            'recaptcha_public_key',
            'recaptcha_default_action',
            'recaptcha_score_threshold',
            'recaptcha_language',
        ]

        widgets = {
            'recaptcha_private_key': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'recaptcha_private_key',
            }),
            'recaptcha_public_key': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'recaptcha_public_key',
            }),
            'recaptcha_default_action': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'recaptcha_default_action',
            }),
            'recaptcha_score_threshold': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'recaptcha_score_threshold',
            }),
            'recaptcha_language': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'recaptcha_language',
            }),
        }
      

class EmailSettingsForm(forms.ModelForm):
    class Meta:
        model = EmailSettings
        fields = [
            'host',
            'host_user',
            'host_password',
            'host_from',
            'host_port',
            'use_ssl',
            'use_tls',

        ]

        widgets = {
            'host': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'host',
            }),
            'host_user': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'host_user',
            }),
            'host_password': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'host_password',
            }),
            'host_from': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'host_from',
            }),
            'host_port': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'host_port',
            }),
        }
      



class SetupForm(forms.ModelForm):
    text = forms.CharField(label='Текст на главной', required=False, widget=CKEditorUploadingWidget())
    
    class Meta:
        model = BaseSettings
        fields = [
            'name',
            'phone',
            'whatsapp',
            'email',
            'email_for_order',
            'copy_year',
            'copy',
            
            'address',
            'work_time',
            'telegram_bot',
            'telegram_group',
            
            'meta_title',
            'meta_description',
            'meta_keywords',
            'text',
            'social_image',
            'logo_light',
            'logo_dark',
            'icon_ico',
            'icon_png',
            'icon_svg',
            'theme_color',
            'active',
            'debugging_mode'
         
            
            ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Название сайта',
                
            }),
            'phone': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Телефон',
                
            }),
            'whatsapp': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Whatsapp',
                
            }),
            'work_time': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Время работы',
                
            }),
            'text': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Время работы',
                
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input',
                'placeholder': 'Email для клиентов'
            }),
            'email_for_order': forms.EmailInput(attrs={
                'class': 'input',
                'placeholder': 'Email для заявок'
            }),
            'copy_year': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Год копирайта',
                
            }),
            'telegram_bot': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Телеграм бот',
                
            }),
            'telegram_group': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Группа телеграм',
                
            }),
            'copy': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Копирайт',
                
            }),
            'address': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Адрес',
                
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Мета заголовок',
                
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'input',
                'placeholder': 'Мета описание',
                
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Ключевые слова',
                
            }),
            'theme_color': forms.TextInput(attrs={
                
                'placeholder': 'Основной цвет',
                'type': 'color'
                
            }),
           
           
        }
        labels = {
            'name': 'Название сайта',
            'phone': 'Телефон',
            'whatsapp': 'Whatsapp',
            'email': 'Email для клиентов',
            'email_for_order': 'Email для заявок',
            'copy_year': 'Год копирайта',
            'copy': 'Копирайт',
            'address': 'Адрес',
            'telegram_bot': 'Телеграм бот',
            'telegram_group': 'Группа телеграм',
            'text': 'Текст на главной',
            
            'meta_title': 'Мета заголовок',
            'meta_description': 'Мета описание',
            'meta_keywords': 'Ключевые слова',
            'social_image': 'Изображение для соц.сетей',
            'logo_light': 'Логотип светлый',
            'logo_dark': 'Логотип темный',
            'icon_ico': 'Иконка .ico',
            'icon_png': 'Иконка .png',
            'icon_svg': 'Иконка .svg',
            'theme_color': 'Основной цвет',
            'active': 'Разрешить индексацию',
            'debugging_mode': 'Режим разработки (вывод текстовой информации об ошибках)',
           
        }