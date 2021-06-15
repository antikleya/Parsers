# -*- coding: utf-8 -*-

import nordvpn_switcher as ns
from random_user_agent.user_agent import UserAgent
from settings import ChitaiGorod_headers
from DetMir import get_json_data
from core import write_dict, get_new_headers, get_new_session, user_agent_rotator
from bs4 import BeautifulSoup
import cfscrape


target_url = "https://market.yandex.ru/catalog--mobilnye-telefony/54726/list?hid=91491&cpa=0&onstock=1&local-offers-first=0"   # replace url with anti-bot protected website
scraper = cfscrape.create_scraper()
html_text = scraper.get(target_url).text
parsed_html = BeautifulSoup(html_text, 'html.parser')
with open('output.txt', 'w') as file:
    file.write(parsed_html.prettify())

