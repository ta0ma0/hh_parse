import requests
import pandas as pd
import sys
from  bs4 import BeautifulSoup
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from config import MY_COOKIE


number_pages = 15
main_vacations_pages = []

for num in (number for number in range(number_pages)):
    url = f'https://spb.hh.ru/search/vacancy?from=resumelist&text=&forceFiltersSaving=true&resume=3747d426ff0378d14f0039ed1f786d526a6732&only_with_salary=true&specialization=1.211&employment=full&page={num}'
    # print(url)
    headers = {'authority': 'spb.hh.ru', 'user-agent': 'Slow wired parser, for my personal comfort (0.1)', 'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
                'cookie': MY_COOKIE}
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
    s.mount('https://', HTTPAdapter(max_retries=retries))
    page = s.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    main_vacations_pages.append(soup.find("div", {"class": "vacancy-serp"}))
    print(soup)
    main_price = []
    main_div = []
    main_vacations_items = []
    # main_price = main_vacations_list.
    # main_vacations_items.append(main_vacations.findAll("div", {"class": "vacancy-serp-item"}))  
    time.sleep(2)

main_vacations_items = []
for div in main_vacations_pages:
    main_vacations_items.append(div.find_all("div", {"class": "vacancy-serp-item"}))

# for el in main_vacations_items:
# print(len(el))


span_salary = []
for span in main_vacations_items:
    for el in span:
        span_salary.append(el.find("span", {"data-qa": "vacancy-serp__vacancy-compensation"}))
    # print(span)

for el in span_salary:
    print(el.text)
    