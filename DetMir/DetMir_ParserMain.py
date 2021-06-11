import requests
from bs4 import BeautifulSoup
# import nordvpn_switcher as ns
from settings import DetMir_headers, detmir_table_structure
from random_user_agent.user_agent import UserAgent
from core import save_row, save_options, write_dict
import json

user_agent_rotator = UserAgent()
temp_url = 'https://www.detmir.ru/catalog/index/name/sortforbrand/brand/13201/page/1/'


def get_new_session():
    """
    Makes a new session

    :return: New session
    :rtype: requests.Session
    """

    # ns.rotate_VPN()
    session = requests.Session()
    session.headers = DetMir_headers
    user = user_agent_rotator.get_random_user_agent()
    session.headers['User-Agent'] = user
    session.get('https://detmir.ru')
    return session


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


def get_name():
    pass


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


# ns.initialize_VPN(save=1, area_input=['complete rotation'], stored_settings=1)

temp_session = get_new_session()
json_data = get_json_data(url='https://www.detmir.ru/catalog/index/name/sortforbrand/brand/13201/page/1/',
                          session=temp_session)
write_dict(json_data['catalog']['data'])
# response = temp_session.get(temp_url).text
# soup = BeautifulSoup(response, 'html.parser')
# script = soup.find('script')
# scripts = soup.find_all('script')
# with open('output.txt', 'w') as file:
#     for script in scripts:
#         if 'Пособие Айрис ПРЕСС' in str(script):
#             file.write(script.prettify())
# write_dict(data)

# ns.terminate_VPN()
