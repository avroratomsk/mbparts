


from decimal import Decimal
import requests
import json
from api.models import Diapasone

def get_diapasone(n):
    diapasones = Diapasone.objects.all()
    for diap in diapasones:
        if diap.start <= n <= diap.end:
            return diap
    return None


login = 'zhitckow2012'
password = '123456'


url = 'https://api.shate-m.ru/api/v1/auth/login'
payload = 'Login=zhitckow2012&Password=123456'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
}

def get_access_token():

    response = requests.post(url, headers=headers, data=payload)
    access_token = ''
    if response.status_code == 200:
        response_data = json.loads(response.text)
        access_token = response_data['access_token']
        # print (access_token)
        
    else:
        print('Ошибка выполнения запроса:', response.status_code)

    return access_token


headers = {
    'accept': 'text/plain',
    'Authorization': 'Bearer ' + get_access_token()
}






from datetime import datetime

def get_search_results(search_string):

    url_search = 'https://api.shate-m.ru/api/v1/articles/search'
    
    # include = 'trademark,contents,extended_info'

    params = {
        'searchString': search_string,
        
    }

    response = requests.get(url_search, headers=headers, params=params)
    data = response.json()
   
    parsed_parts = []
    for item in data:

        try:
            parsed_part = {}

            id = item['article']['id']
            name = item['article']['name']
            brand = item['article']['tradeMarkName']
            

            parsed_part['id'] = id
            parsed_part['name'] = name
            parsed_part['brand'] = brand
            parsed_part['supplier'] = 'shate-m.ru'
            parsed_part['count'] = 0
            parsed_part['price'] = 0
            parsed_part['date'] = 0
            price_data = [
                {
                "articleId": id,
                "includeAnalogs": False
                }
            ]
            price_response = requests.post('https://api.shate-m.ru/api/v1/prices/search', headers=headers, json=price_data)
            price_data = price_response.json()
            for price in price_data:
                price_value = price['price']['value']
                delivery = price['shippingDateTime']

                current_date = datetime.utcnow()
                target_date = datetime.strptime(delivery, '%Y-%m-%dT%H:%M:%SZ')
                delta = target_date - current_date
                delta_days = int(delta.total_seconds() / 86400)

                parsed_part['count'] = price['quantity']['available']
                x = Decimal(parsed_part['price']).quantize(Decimal(1))
                persent = get_diapasone(x)
                
                try:
                    parsed_part['price'] = float(price_value) + float((price_value/100)*persent.persent)
                    

                except:
                    

                    parsed_part['price'] = price_value


                parsed_part['date'] = delta_days

            parsed_parts.append(parsed_part)
        except:
            pass

    
    return parsed_parts


# print(get_search_results('c110'))
# get_search_results('c110')



