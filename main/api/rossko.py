

import csv
import requests
import urllib
import os
from pytils.translit import slugify

import datetime
from decimal import Decimal

from api.models import Diapasone


# росско
# key1: a81ef8d8be44d645bf0c64edd2446a46
# key2: 21ec262ac9a098ce11ebf635dce62f30



price_url = 'https://webprice.rossko.ru/service/getPriceList.php?t=%D0%9E%D0%A2-000044'

search_url = 'http://api.rossko.ru/service/v2.1/GetSearch'




def savePrice():
    date = datetime.datetime.now()
    print(date)
    pdf_file = urllib.request.urlopen(price_url)
    with open('price.xlsx','wb') as output:
        output.write(pdf_file.read())


# savePrice()
from zeep import Client
headers = {'content-type': 'text/xml'}
client = Client(search_url)


def get_diapasone(n):
    diapasones = Diapasone.objects.all()
    for diap in diapasones:
        if diap.start <= n <= diap.end:
            return diap
    return None


import json

def rossko_search(query):

    KEY1 = '7d46675a2c0f8864368ffa9ad8836f98'
    KEY2 = '701e257a5f1f87324b0ddbb0f4eb63a1'

    connect = {
        'wsdl': 'http://api.rossko.ru/service/v2.1/GetCheckoutDetails',
        'options': {
            'timeout': 1,
            'trace': True
        }
    }

    param_del = {
        'KEY1': KEY1,
        'KEY2': KEY2
    }

    client_del = Client(connect['wsdl'])
    del_result = client_del.service.GetCheckoutDetails(**param_del)

    

    params = {
        'KEY1': KEY1,
        'KEY2': KEY2,
        'text': query,
        'delivery_id': '000000002',   
        'address_id': del_result['DeliveryAddress']['address'][0]['id']
    }

    result = client.service.GetSearch(**params)

    
    
    
    try:
        parts = result.PartsList.Part
        parsed_parts = []

        for part in parts:
            parsed_part = {}
            
            parsed_part['name'] = part.name
            parsed_part['brand'] = part.brand
            parsed_part['supplier'] = 'rossko.ru'
            parsed_part['count'] = 0
            parsed_part['price'] = 0
            parsed_part['date'] = 0
            
            if hasattr(part, 'stocks'):
                try:
                    stocks = part.stocks.stock
                    for stock in stocks:
                        parsed_part['date'] = stock.delivery + 1
                        parsed_part['count'] += stock.count
                        parsed_part['price'] += float(stock.price)
                        parsed_part['id'] = stock.id

                    x = Decimal(parsed_part['price']).quantize(Decimal(1))
                    persent = get_diapasone(x)
                    
                    try:
                        parsed_part['price'] = float(parsed_part['price']) + float((parsed_part['price']/100)*persent.persent)
                        

                    except:
                        pass
                    
                except Exception as e:
                    print(e)
                    stocks = None
                
            parsed_parts.append(parsed_part)
            
            if hasattr(part, 'crosses'):
                try:
                    crosses = part.crosses.Part
                    for cross in crosses:
                        parsed_cross = {}
                        
                        parsed_cross['name'] = cross.name
                        parsed_cross['brand'] = cross.brand
                        parsed_cross['supplier'] = 'rossko.ru'
                        parsed_cross['count'] = 0
                        parsed_cross['price'] = 0
                        parsed_cross['date'] = 0

                        if hasattr(cross, 'stocks'):
                            try:
                                stocks = cross.stocks.stock
                                for stock in stocks:
                                    parsed_cross['date'] = stock.delivery + 1
                                    parsed_cross['count'] += stock.count
                                    parsed_cross['price'] += float(stock.price)
                                    parsed_cross['id'] = stock.id
                                x = Decimal(parsed_cross['price']).quantize(Decimal(1))
                                persent = get_diapasone(x)

                                try:
                                    parsed_cross['price'] = float(parsed_cross['price']) + float((parsed_cross['price']/100)*persent.persent)

                                except:
                                    pass

                            except Exception as e:
                                print(e)
                                stocks = None

                        parsed_parts.append(parsed_cross)
                    
                except Exception as e:
                    print(e)
                    crosses = None


    except Exception as e:
        print(e)
        parsed_parts = []
    
    
    return parsed_parts




# print(rossko_search('c110'))