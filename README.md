        

### НАСТРОЙКА БЭКА ###
## в папке main/main создаем 2 файла:
static_setup.py
set_whitenoise.py


## Содержимое static_setup.py:
from .local_settings import STATIC_URL
from .local_settings import STATICFILES_DIRS
from .local_settings import MEDIA_URL
from .local_settings import MEDIA_ROOT


## Содержимое set_whitenoise.py:
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


## в папке main/admin создаем файл со следующим содержимым
folder = 'csv_upload/'


## Создаем копию файла local_settings и дописиваем ему расширение .py
## В файле local_settings.py меняем пути на пути до проекта


## Через консоль/терминал в папке прокета устанавливаем виртуальное окружение
python -m venv venv

## Активируем его
source venv/biv/activate

## проверяем правильно ли определился путь до pip:
which pip

## Устанавливаем зависимости
pip install -r requirements.txt

## Переходим в папку main
cd main

## Создаем миграции каждого приложения
python manage.py makemigrations accounts
python manage.py makemigrations blog
python manage.py makemigrations coupons
python manage.py makemigrations home
python manage.py makemigrations orders
python manage.py makemigrations pay
python manage.py makemigrations serv
python manage.py makemigrations setup
python manage.py makemigrations shop


## Примеряем миграции
python manage.py migrate

# Создаем суперпользователя
python manage.py createsuperuser

# Запускаем бэк проекта 
python manage.py runserver 





### УСТАНОВКА ФРОНТЕНДА  ###

* введите ```yarn set version berry```
* скачайте необходимые зависимости: ```yarn```
* чтобы начать работу, введите команду: ```yarn run dev``` (режим разработки)





## Для работы нужно в ДВУХ разных терминалах из папки проекта запустить 2 процесса. Один отвечает за бэк, второй за фронт.
## Открываем первый терминал и переходим в папку main. Запускаем:
python manage.py runserver 

## Во втором терминале из корня проекта запускаем
yarn run dev


### РАБОТАЕМ! ###
