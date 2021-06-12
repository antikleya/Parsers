from core import write_dict, get_new_headers
from random_user_agent.user_agent import UserAgent
from settings import YandexMarket_headers
from bs4 import BeautifulSoup
import nordvpn_switcher as ns
import requests

temp_url = 'https://market.yandex.ru/catalog--smartfony/16814639/list?glfilter=4940921%3A13475069&hid=91491'
user_agent_rotator = UserAgent()
ns.initialize_VPN(save=1, area_input=['complete rotation'])
headers = get_new_headers(YandexMarket_headers, user_agent_rotator)
session = requests.Session()
headers['User-Agent'] = user_agent_rotator.get_random_user_agent()

session.headers = headers
response = session.get('https://market.yandex.ru/catalog--smartfony/16814639/list?glfilter=4940921%3A13475069&hid=91491').text
ns.rotate_VPN()
soup = BeautifulSoup(response, 'lxml')
if 'Смартфон Xiaomi' in soup.text:
    print('yes')

ns.terminate_VPN()
