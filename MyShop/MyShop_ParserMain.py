from bs4 import BeautifulSoup
import requests
import json
from core import save_row, save_options, create_table
from settings import myshop_table_structure

temp_url = 'https://my-shop.ru/shop/producer/149/sort/b/page/'


def get_lower_price(product):
    price = product['cost']
    return str(price)


def get_sale_percentage(product):
    if product['promos']:
        return str(product['promos'][0]['discount'])
    else:
        return '0'


def get_non_sale_price(product):
    if product['old_cost'] is None:
        return get_lower_price(product)
    else:
        return str(product['old_cost'])


def get_brand(product):
    brand = product['ga_item']['brand']
    return brand


def get_image_src(product):
    image_src = f"https:{product['image']['href']}"
    return image_src


def get_name(product):
    name = product['ga_item']['name']
    return name


def get_json_data(url):
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'html.parser')
    json_text = str(soup.find_all('script')[1])
    json_text = json_text[json_text.find('{'):json_text.rfind('};') + 1]
    json_data = json.loads(json_text)
    return json_data['response']


def get_series(json_data):
    for i in json_data['product']['about']:
        if i['name'] == 'серия':
            return i['value']
    return ''


def get_isbn(json_data):
    for characteristic in json_data['product']['characteristics']:
        if characteristic['name'] == 'ISBN':
            return characteristic['value']
    return ''


def get_url(base_url, page_number):
    return f"{base_url}{page_number}.html"


def get_page_amount(base_url):
    url = get_url(base_url, 1)
    json_data = get_json_data(url)
    page_amount = json_data['meta']['total']
    if page_amount % 36 == 0:
        return page_amount // 36
    return page_amount // 36 + 1


def get_article(product):
    article = product['product_id']
    return str(article)


def get_product_info(product, current_page_number, product_position):
    brand = get_brand(product)
    lower_price = get_lower_price(product)
    non_sale_price = get_non_sale_price(product)
    sale_percentage = get_sale_percentage(product)
    article = get_article(product)
    popularity = product_position + 1 + 36 * (current_page_number - 1)
    image_src = get_image_src(product)
    name = get_name(product)
    product_url = f"https://my-shop.ru/shop/product/{article}.html"
    json_data = get_json_data(product_url)
    series = get_series(json_data)
    isbn = get_isbn(json_data)
    row = (brand, name, series, non_sale_price, sale_percentage, lower_price, popularity, image_src,
           article, isbn)
    return row


def parse_page(base_url, current_page_number, save_option, table_name=''):
    page_url = get_url(base_url, current_page_number)
    print(page_url)
    json_data = get_json_data(page_url)
    for i in range(len(json_data['products'])):
        row = get_product_info(json_data['products'][i], current_page_number, i)
        save_row(row, table_name, save_option, myshop_table_structure)


def run_parser(url, save_option):
    table_flag = False
    if save_option == save_options['.db']:
        table_name = create_table(myshop_table_structure)
        table_flag = True
    page_amount = get_page_amount(url)
    for i in range(1, page_amount + 1):
        if table_flag:
            parse_page(url, i, save_option, table_name)
        else:
            parse_page(url, i, save_option)
    input('Нажмите enter для выхода: ')


if __name__ == '__main__':
    run_parser(temp_url, save_options['.db'])
