# -*- coding: utf-8 -*-
from core import write_dict, get_new_headers, get_new_session
from random_user_agent.user_agent import UserAgent
from settings import Ozon_headers
from bs4 import BeautifulSoup
import nordvpn_switcher as ns

ns.initialize_VPN(stored_settings=1)
ns.rotate_VPN()

temp_url = 'https://www.ozon.ru/publisher/ayris-press-857416/'
user_agent_rotator = UserAgent()
headers = get_new_headers(Ozon_headers, user_agent_rotator)

session = get_new_session('https://www.ozon.ru', headers)

response = session.get(temp_url).text
soup = BeautifulSoup(response, 'lxml')
print(soup.prettify())

with open('temp.txt', 'w') as file:
    file.write(soup.prettify())

ns.terminate_VPN()
