from bs4 import BeautifulSoup
# import nordvpn_switcher as ns
from settings import DetMir_headers, detmir_table_structure
from random_user_agent.user_agent import UserAgent
from core import save_row, save_options, write_dict, get_new_session, get_new_headers
import json

user_agent_rotator = UserAgent()
temp_url = 'https://www.detmir.ru/catalog/index/name/sortforbrand/brand/13201/page/1/'


def get_json_data(url, session):
    """
    Gets initial json data of the given page

    :param url: Must be a correct link to a page with product list or an individual product page on detmir.ru
    :param session: requests.Session object of the current session
    :return: Page data converted into python structure
    :rtype: dict
    """

    response = session.get(url).text
    soup = BeautifulSoup(response, 'html.parser')
    json_text = str(soup.find('script', {'id': 'app-data'}))
    json_text = json_text[json_text.find('{'):json_text.rfind("</script>")]
    json_text = json_text.replace('&quot;', '"')
    json_data = json.loads(json_text)
    return json_data


def get_name(product):
    """
    Gets product's name

    :param product: Must be a correct json of product information
    :return: Name
    :rtype: str
    """

    name = product['title']
    return name


def get_lower_price(product):
    """
    Gets product's current price

    :param product: Must be a correct json of product information
    :return: current price
    :rtype: int
    """

    lower_price = product['price']['price']
    return lower_price


def get_non_sale_price(product):
    """
    Gets product's price before sale, if on sale. Otherwise gets current price.

    :param product: Must be a correct json of product information
    :return: non-sale price
    :rtype: int
    """

    if product['old_price']:
        old_price = product['old_price']['price']
        return old_price
    return get_lower_price(product)


def get_sale_percentage(lower_price, non_sale_price):
    """
    Calculates sale percentage from prices

    :param lower_price: current product price
    :param non_sale_price: product's price before sale
    :return: sale percentage
    :rtype: int
    """

    sale_percentage = round((1-(lower_price/non_sale_price))*100)
    return sale_percentage


def get_rating(product):
    """
    Gets rating of a product

    :param product: Must be a correct json of product information
    :return: rating
    :rtype: str
    """

    rating = str(product['rating'])
    return rating


def get_review_amount(product):
    """
    Gets the amount of reviews for a given product

    :param product: Must be a correct json of product information
    :return: review amount
    :rtype: int
    """

    review_amount = product['review_count']
    return review_amount


def get_image_src(product):
    """
    Gets image links of a given products

    :param product: Must be a correct json of product information
    :return: image links
    :rtype: str
    """

    image_src = ''
    for picture in product['pictures']:
        image_src += picture['original'] + ', '
    if image_src:
        image_src = image_src[:-2]
    return image_src


def get_product_info(product, current_page_number, product_position):
    """
    Gets all required information on a given product

    :param product: Must be a correct json of product information
    :param current_page_number:
    :param product_position: Position of the given product on the page. Indexes start from 0
    :return: Product information in the same order as in database
    :rtype: tuple
    """

    # brand = get_brand(product)
    name = get_name(product)
    lower_price = get_lower_price(product)
    non_sale_price = get_non_sale_price(product)
    sale_percentage = get_sale_percentage(lower_price, non_sale_price)
    popularity = product_position + 1 + 30 * (current_page_number - 1)
    rating = get_rating(product)
    review_amount = get_review_amount(product)
    image_src = get_image_src(product)
    # article = get_article(product)
    #
    #
    #
    # product_url = f"https://my-shop.ru/shop/product/{article}.html"
    # json_data = get_json_data(product_url)
    # series = get_series(json_data)
    # isbn = get_isbn(json_data)
    # row = (brand, name, series, non_sale_price, sale_percentage, lower_price, popularity, image_src,
    #        article, isbn)
    # return row


def parse_page(base_url, current_page_number, save_option, table_name=''):
    """
    Parses all products on the given page

    :param base_url: Must be a url in the form of 'https://my-shop.ru/*/page'
    :param current_page_number:
    :param save_option: Must be a supported save option from 'save_options' dict
    :param table_name: If saving into sql db, must be a name of an existing table in the database
    :return:
    """

    pass
    # page_url = get_url(base_url, current_page_number)
    # print(page_url)
    # json_data = get_json_data(page_url)
    # for i in range(len(json_data['products'])):
    #     row = get_product_info(json_data['products'][i], current_page_number, i)
    #     save_row(row, table_name, save_option, detmir_table_structure)


if __name__ == '__main__':

    # ns.initialize_VPN(save=1, area_input=['complete rotation'], stored_settings=1)
    headers = get_new_headers(headers=DetMir_headers, user_agent_rotator=user_agent_rotator)
    session = get_new_session(url='https://detmir.ru', headers=headers)
    json_data = get_json_data(url='https://www.detmir.ru/catalog/index/name/sortforbrand/brand/13201/page/1/',
                              session=session)
    # # print(json_data['catalog']['data'].keys())
    # # write_dict(json_data['catalog']['data']['items'][0])
    item = json_data['catalog']['data']['items'][0]
    # write_dict(data)

    print(type(get_review_amount(item)))
    # ns.terminate_VPN()
