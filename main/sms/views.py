from django.shortcuts import render

# Create your views here.
import requests
from setup.models import BaseSettings

try:
    sms = BaseSettings.objects.get().sms
except:
    sms = False

sender = 'INFO'
apikey = 'OUP72K92NNDIW5903S155P8J3XAREYI7D1490E1HSI0F27T1XO2T7S97A17CWDQW'


def send_sms(text, phone):
    url = "http://smspilot.ru/api.php?send="+text+"&to="+phone+"&apikey="+apikey+"&format=json"
    
    # result = requests.get(url)
    pass