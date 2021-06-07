import sqlite3

from bs4 import BeautifulSoup
from requests import get
from datetime import datetime


def db_save(row, table_name):
    connection = sqlite3.connect('../ParsingResults.db')
    cursor = connection.cursor()
    cursor.execute(f"INSERT or REPLACE INTO {table_name} VALUES (?,?,?,?,?,?,?,?)",
                   (row['brand'] + row['name'], row['lower_price'], row['sale_percentage'], row['non_sale_price'],
                    row['popularity'], row['rating'], row['review_amount'], row['article']))


save_options = {'.db': db_save}


def create_table():
    date = datetime.today().strftime('%d_%m_%Y_%H_%M')
    table_name = f'WildBerries_{date}'
    connection = sqlite3.connect('../ParsingResults.db')
    cursor = connection.cursor()
    cursor.execute(f"""CREATE TABLE {table_name} (
            Название               STRING,
            Цена                   STRING,
            Скидка                 STRING,
            Итого                  STRING,
            [Популярность рейтинг] STRING,    
            Рейтинг                STRING,
            Отзывы                 STRING,
            Артикул                STRING UNIQUE
                                          NOT NULL
        );
        """)
    connection.commit()
    connection.close()
    return table_name


def get_elements(url):
    response = get(url).text
    soup = BeautifulSoup(response, 'html.parser')
    elements = soup.find_all('a', class_='ref_goods_n_p j-open-full-product-card')
    return elements


def space_delete(inp):
    if inp[0] == ' ':
        return inp[1:]
    return inp


def get_lower_price(element):
    price = element.find('ins', class_='lower-price')
    if price is None:
        price = element.find('span', class_='lower-price')
    return space_delete(price.text)


def get_sale_percentage(element):
    sale = element.find('span', class_='price-sale active')
    if sale is None:
        return '0%'
    return space_delete(sale.text)


def get_non_sale_price(element):
    non_sale_price = element.find('span', class_='price-old-block')
    if non_sale_price is None:
        return get_lower_price(element)
    return space_delete(non_sale_price.find('del').text)


def get_rating(element):
    rating = element.find('span', class_='c-stars-line-lg')
    if rating is None:
        return 'Нет'
    return rating['class'][-1][-1]


def get_brand(element):
    brand = element.find('strong', class_='brand-name')
    return brand.text


def get_review_amount(element):
    review_amount = element.find('span', class_='dtList-comments-count')
    if review_amount is None:
        return '0'
    return review_amount.text


def get_article(element):
    article = element['href'].split('/')[2]
    return article


def get_page_amount(url):
    response = get(url).text
    soup = BeautifulSoup(response, 'html.parser')
    count = soup.find('span', class_='goods-count j-goods-count').text[5:]
    count = count.split()
    count = int(''.join(count[:len(count)-1]))
    if count % 100 == 0:
        return count // 100
    return (count // 100) + 1


def get_name(url):
    response = get(url).text
    soup = BeautifulSoup(response, 'html.parser')
    name = soup.find('span', class_='name').text
    return name


def save(row, table_name, save_option):
    if save_option == save_options['.db']:
        save_option(row, table_name)


def parse_page(base_url, current_page_number, save_option, table_name=''):
    url = base_url + f'&page={current_page_number}'
    print(url)
    elements = get_elements(url)
    for i in range(len(elements)):
        row = {'lower_price': get_lower_price(elements[i]),
               'non_sale_price': get_non_sale_price(elements[i]),
               'rating': get_rating(elements[i]),
               'brand': get_brand(elements[i]),
               'sale_percentage': get_sale_percentage(elements[i]),
               'review_amount': get_review_amount(elements[i]),
               'article': get_article(elements[i]),
               'popularity': i + 100 * (current_page_number - 1)}
        product_url = f'https://www.wildberries.ru/catalog/{row["article"]}/detail.aspx'
        row['name'] = get_name(product_url)
        save(row, table_name, save_option)


def run_parser(url, save_option):
    table_flag = False
    if save_option == save_options['.db']:
        table_name = create_table()
        table_flag = True
    page_amount = get_page_amount(url)
    for i in range(1, page_amount + 1):
        if table_flag:
            parse_page(url, i, save_option, table_name)
        else:
            parse_page(url, i, save_option)


run_parser('https://www.wildberries.ru/catalog/0/search.aspx?search=%D0%B0%D0%BD%D0%B8%D0%BC%D0%B5&xsearch=true',
           save_options['.db'])
