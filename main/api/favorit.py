from decimal import Decimal
import requests

api_key = '9D728727-0BBF-4959-A9A0-3FE7E18EC3CD'


from api.models import Diapasone
def get_diapasone(n):
    diapasones = Diapasone.objects.all()
    for diap in diapasones:
        if diap.start <= n <= diap.end:
            return diap
    return None

from datetime import datetime, timezone

def get_favorit_get(query):
    url = f'https://api.favorit-parts.ru/hs/hsprice/?key={api_key}&number=' + query
    response = requests.get(url)   


    parsed_parts = []
    data = response.json()

    

    for item in data['goods']:
        

        try:
            parsed_part = {}
            id = item['number']
            brand = item['brand']

            parsed_part['id'] = item['number']
            parsed_part['brand'] = item['brand']
            parsed_part['name'] = item['name']
            parsed_part['supplier'] = 'favorit.ru'
            parsed_part['count'] = item['warehouses'][0]['stock']
            parsed_part['price'] = item['price']
            x = Decimal(parsed_part['price']).quantize(Decimal(1))
            persent = get_diapasone(x)
            
            try:
                parsed_part['price'] = float(parsed_part['price']) + float((parsed_part['price']/100)*persent.persent)
                

            except:
                pass
        

            current_date = datetime.now(timezone.utc)
            target_date = datetime.strptime(item['warehouses'][0]['shipmentDate'], '%Y-%m-%dT%H:%M:%S%z')
            target_date = target_date.replace(tzinfo=timezone.utc)
            delta = target_date - current_date
            delta_days = delta.days

            parsed_part['date'] = delta_days

            parsed_parts.append(parsed_part)

            
            analog_url = f'http://api.favorit-parts.ru/hs/hsprice/?key={api_key}&number={id}&brand={brand}&analogues=on'
            analog_response = requests.get(analog_url) 
            analog_data = analog_response.json()

            


            # for item in analog_data['goods'][0]['analogues']:

            #     try:

            #         parsed_cross = {}
            #         parsed_cross['id'] = item['number']
            #         parsed_cross['brand'] = item['brand']
            #         parsed_cross['name'] = item['name']
            #         parsed_cross['supplier'] = 'favorit.ru'
            #         parsed_cross['count'] = item['warehouses'][0]['stock']
            #         parsed_cross['price'] = item['price']

            #         current_date = datetime.now(timezone.utc)
            #         target_date = datetime.strptime(item['warehouses'][0]['shipmentDate'], '%Y-%m-%dT%H:%M:%S%z')
            #         target_date = target_date.replace(tzinfo=timezone.utc)
            #         delta = target_date - current_date
            #         delta_days = delta.days

            #         parsed_cross['date'] = delta_days

            #         parsed_parts.append(parsed_part)
            #     except:
            #         pass


        except Exception as e:
            print(e)
            pass

    
    # print(parsed_parts)
    return parsed_parts



# get_favorit('NSII0001047309')