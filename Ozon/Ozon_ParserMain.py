# -*- coding: utf-8 -*-
from core import user_agent_rotator, get_new_headers, get_new_session, save_options, save_row, create_table, \
    get_str_table_struct
from settings import Ozon_headers, ozon_table_structure
from bs4 import BeautifulSoup
import json
import re
# import nordvpn_switcher as ns
# ns.initialize_VPN(save=1, area_input=['complete rotation'])
# ns.rotate_VPN()

temp_url = 'https://www.ozon.ru/publisher/ayris-press-857416/'


def get_json_data(url, session):
    """
    Gets initial json data of the given page

    :param url: Must be a correct link to a page with product list or an individual product page on ozon.ru
    :param session: requests.Session object of the current session
    :return: Page data converted into python structure
    :rtype: dict
    """

    response = session.get(url=url, timeout=10).text
    soup = BeautifulSoup(response, 'lxml')
    json_text = soup.find('div', {'id': 'state-searchResultsV2-312617-default-1'})
    if not json_text:
        json_text = soup.find('div', {'id': 'state-searchResultsV2-312864-default-1'})
    json_text = json_text['data-state']
    json_data = json.loads(json_text)
    return json_data


def get_name(product):
    """
    Gets product's name

    :param product: Must be a correct json of product information
    :return: Name
    :rtype: str
    """

    name = product['cellTrackingInfo']['title']
    return name


def get_lower_price(product):
    """
    Gets product's current price

    :param product: Must be a correct json of product information
    :return: current price
    :rtype: int
    """

    lower_price = product['cellTrackingInfo']['finalPrice']
    return lower_price


def get_non_sale_price(product):
    """
    Gets product's price before sale, if on sale. Otherwise gets current price.

    :param product: Must be a correct json of product information
    :return: non-sale price
    :rtype: int
    """

    non_sale_price = product['cellTrackingInfo']['price']
    return non_sale_price


def get_sale_percentage(product):
    """
    Calculates sale percentage from prices

    :param product: Must be a correct json of product information
    :return: sale percentage
    :rtype: int
    """

    sale_percentage = product['cellTrackingInfo']['discount']
    return sale_percentage


def get_rating(product):
    """
    Gets rating of a product

    :param product: Must be a correct json of product information
    :return: rating
    :rtype: str
    """

    rating = str(product['cellTrackingInfo']['rating'])[:5]
    return rating


def get_type(product):

    product_type = product['type']
    return product_type


def get_review_amount(product):
    """
    Gets the amount of reviews for a given product

    :param product: Must be a correct json of product information
    :return: review amount
    :rtype: int
    """

    review_amount = product['cellTrackingInfo']['countItems']
    return review_amount


def get_image_src(product):
    """
    Gets image links of a given products

    :param product: Must be a correct json of product information
    :return: image links
    :rtype: str
    """

    image_src = ', '.join(product['images'])
    return image_src


def get_product_code(product):
    """
    Gets code of a given product on the site

    :param product: Must be a correct json of product information
    :return: product code
    :rtype: int
    """

    product_code = product['cellTrackingInfo']['id']
    return product_code


def get_article(product):
    """
    Gets article of a given product

    :param product: Must be a correct json of product information
    :return: article
    :rtype: str
    """

    article = product['cellTrackingInfo']['marketplaceSellerId']
    return article


def get_availability(product):
    """
    Gets warehouse codes where the given product is available

    :param product: Must be a correct json of product information
    :return: availability
    :rtype: str
    """

    availability = product['cellTrackingInfo']['availability']
    return availability


def get_url(base_url, current_page_number):
    """
    Makes a concrete page url from base url and page number

    :param base_url: Must be a url in the form of 'https://www.ozon.ru/*/'
    :param current_page_number:
    :return: page url
    :rtype: str
    """

    url = f'{base_url}?page={current_page_number}'
    return url


def get_page_amount(url, session):
    """
    Gets amount of product pages

    :param url: first page url
    :param session: requests.Session object of the current session
    :return: page amount
    :rtype: int
    """

    response = session.get(url=url, timeout=2).text
    page_amount = re.search('''"totalPages":\d+''', response).group()
    page_amount = page_amount[page_amount.find(':') + 1:]
    return int(page_amount)


def get_product_info(product, current_page_number, product_position):
    """
    Gets all required information on a given product

    :param product: Must be a correct json of product information
    :param current_page_number:
    :param product_position: Position of the given product on the page. Indexes start from 0
    :return: Product information in the same order as in database
    :rtype: tuple
    """

    name = get_name(product)
    non_sale_price = get_non_sale_price(product)
    sale_percentage = get_sale_percentage(product)
    lower_price = get_lower_price(product)
    popularity = product_position + 1 + 36 * (current_page_number - 1)
    product_type = get_type(product)
    rating = get_rating(product)
    review_amount = get_review_amount(product)
    image_src = get_image_src(product)
    product_code = get_product_code(product)
    article = get_article(product)
    availability = get_availability(product)
    row = (name, non_sale_price, sale_percentage, lower_price, popularity, product_type, rating, review_amount,
           image_src, product_code, article, availability)
    return row


def parse_page(base_url, current_page_number, save_option, session, table_name=''):
    """
    Parses all products on a given page

    :param base_url: Must be a url in the form of 'https://www.ozon.ru/*/'
    :param current_page_number:
    :param save_option: Must be a supported save option from 'save_options' dict
    :param session: requests.Session object of the current session
    :param table_name: If saving into sql db, must be a name of an existing table in the database
    :return:
    """

    page_url = get_url(base_url, current_page_number)
    print(page_url)
    json_data = get_json_data(url=page_url, session=session)
    for i in range(len(json_data['items'])):
        row = get_product_info(json_data['items'][i], current_page_number, i)
        save_row(row, table_name, save_option, ozon_table_structure)


def run_parser(base_url, save_option):
    """
    Main function of the parser. Gets all products information from the given list and saves it according to
    the chosen save option

    :param base_url: Must be a url in the form of 'https://www.ozon.ru/*/'
    :param save_option: Must be a supported save option from 'save_options' dict
    :return:
    """

    url = get_url(base_url, 1)
    headers = get_new_headers(Ozon_headers, user_agent_rotator)
    session = get_new_session(url=url, headers=headers)

    table_name = ''
    if save_option == save_options['.db']:
        table_name = create_table(ozon_table_structure, 'Ozon')

    page_amount = get_page_amount(url, session)
    for i in range(1, page_amount + 1):
        parse_page(base_url, i, save_option, session, table_name)

    input('Нажмите enter для выхода: ')


if __name__ == '__main__':
    # run_parser('https://www.ozon.ru/publisher/ayris-press-857416/', save_options['.db'])
    headers = get_new_headers(Ozon_headers, user_agent_rotator)
    session = get_new_session(temp_url, headers)

    response = session.get('https://www.ozon.ru/publisher/ayris-press-857416/', timeout=4).text
    print(response)
