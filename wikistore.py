import json

import requests
from bs4 import BeautifulSoup

url_main = 'https://wiki.smzdm.com/p/60ryy5o/'

header_main = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

response_main = requests.get(url=url_main, headers=header_main)
soup = BeautifulSoup(response_main.text, 'lxml')
pinpai_img = soup.find('img', attrs={'alt': 'Apple/苹果'})['src']
pinpai_title = soup.find('div', attrs={'class': 'pp-title'}).find('a').text
pinpai_info = soup.find('div', attrs={'class': 'pinpai-info'}).text.strip()
data_aid = str(soup.find('input', attrs={'id': 'data-aid'})['value'])
pinpai = {
    "pinpai_img": pinpai_img,
    "pinpai_title": pinpai_title,
    'pinpai_info': pinpai_info
}
information_div = soup.find('div', attrs={'class': 'sku-types-wrapper'})
cup_id = information_div.find('a', attrs={'class': 'type-item available'})['attr_value_id']
cup_name = information_div.find('a', attrs={'class': 'type-item available'}).text

color_id_list = [information_div.find('a', attrs={'class': 'type-item available'}).find_next('a', attrs={
    'class': 'type-item available'})['attr_value_id'],
                 information_div.find('a', attrs={'class': 'type-item available'}).find_next('a', attrs={
                     'class': 'type-item available'}).find_next('a', attrs={'class': 'type-item available'})[
                     'attr_value_id']]

color_name_list = [information_div.find('a', attrs={'class': 'type-item available'}).find_next('a', attrs={
    'class': 'type-item available'}).text,
                   information_div.find('a', attrs={'class': 'type-item available'}).find_next('a', attrs={
                       'class': 'type-item available'}).find_next('a', attrs={'class': 'type-item available'}).text]

capacity_id_list_tuple = information_div.find('div').find_next_sibling('div').find_next_sibling(
    'div').find_next_sibling('div').find_all('a', attrs={'class': 'type-item available'})
capacity_id_list = [i['attr_value_id'] for i in capacity_id_list_tuple]

capacity_name_list = [i.text for i in capacity_id_list_tuple]

network_id_list_tuple = information_div.find('div').find_next_sibling('div').find_next_sibling('div').find_next_sibling(
    'div').find_next_sibling(
    'div').find_all('a', attrs={'class': 'type-item available'})
network_id_list = [i['attr_value_id'] for i in network_id_list_tuple]
network_name_list = [i.text for i in network_id_list_tuple]

dict_id_name = {
    'cpu': {cup_id: cup_name},
    'color': dict(zip(color_id_list, color_name_list)),
    'capacity': dict(zip(capacity_id_list, capacity_name_list)),
    'network': dict(zip(network_id_list, network_name_list)),
}

information_dict = {
    'cpu': cup_id,
    'color': color_id_list,
    'capacity': capacity_id_list,
    'network': network_id_list
}


# ---------------------------------------------------------------------------------------------------------------------

def get_Product_id(cpu, color, capacity, network, url_referer):
    header_Product = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Referer': url_referer
    }
    url_product = 'https://wiki.smzdm.com/wiki/wiki_attr?hash_id=60ryy5o&attr_value_ids=' + cpu + '%2C' + color + '%2C' + capacity + '%2C' + network + '&first=0'
    data_information = {
        'hash_id': '60ryy5o',
        'attr_value_ids': f'{cpu},{color},{capacity},{network}',
        'first': 0
    }
    response_getProduct = requests.get(url=url_product, headers=header_Product, data=data_information)
    json_Product_id = response_getProduct.json()
    sku_id = json_Product_id['data']['sku'][0]['sku_id']
    return sku_id


id_Product_list = []
id_information_json = []
for capacity in information_dict['capacity']:
    for color in information_dict['color']:
        for network in information_dict['network']:
            id_Product_list.append(
                get_Product_id(str(information_dict['cpu']), str(color), str(capacity), str(network), url_main))
            id_information_json.append(
                {'cpu': dict_id_name['cpu'][str(information_dict['cpu'])], 'color': dict_id_name['color'][color],
                 'capacity': dict_id_name['capacity'][capacity], 'network': dict_id_name['network'][network]})


# ---------------------------------------------------------------------------------------------------------------------

def method_name(id, referer, id_information_json):
    url_getProduct = f'https://wiki.smzdm.com/create/ugc_product/get_related_product_detail?id={id}'
    header_getProduct = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Referer': referer
    }
    data_getProduct = {
        'id': id
    }
    response = requests.get(url=url_getProduct, headers=header_getProduct, data=data_getProduct)
    json_getProduct = response.json()
    dict_getProduct = {
        'pro_id': json_getProduct['data']['pro_id'],
        'pro_name_pro_subtitle': json_getProduct['data']['pro_name'],
        'pro_price': json_getProduct['data']['pro_price'],
        'pro_pic': json_getProduct['data']['pro_pic'],
        'pro_content': json_getProduct['data']['pro_content'],
    }
    id_information_json['pro_id'] = json_getProduct['data']['pro_id']
    id_information_json['pro_price'] = json_getProduct['data']['pro_price']
    id_information_json['pro_pic'] = json_getProduct['data']['pro_pic']
    id_information_json['pro_content'] = json_getProduct['data']['pro_content']
    id_information_json['pro_name_pro_subtitle'] = json_getProduct['data']['pro_name']
    return id_information_json


product_list = []
for i in range(0, len(id_Product_list)):
    product_list.append(method_name(id_Product_list[i], url_main, id_information_json[i]))
dict_var_list = []
for i in product_list:
    dict_var = {
        i['cpu']: {
            i['color']: {
                i['capacity']: {
                    i['network']: {
                        'price': i['pro_price']
                    }
                }
            }
        },
        'info': {
            i['pro_pic']: {
                i['pro_content']: {
                    i['pro_name_pro_subtitle']: {
                        'pro_id': i['pro_id']
                    }
                }
            }
        }
    }
    dict_var_list.append(dict_var)

data_over = {
    'data': dict_var_list,
    'pinpai': pinpai
}
data_json = json.dumps(data_over, sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False)
with open('data.json', 'w', encoding='utf-8') as f:
    f.write(data_json)

