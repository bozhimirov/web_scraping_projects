from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
from requests.structures import CaseInsensitiveDict


driver = webdriver.Chrome()
initial_url = 'https://www.producthunt.com/search/users?q=users&maker=true'
partial_url = 'https://www.producthunt.com/@'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
                 '(KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
headers = {'User-Agent': user_agent}

driver.get(initial_url)


start = time.time()
pages = 1
pages_prod = 49
for page_num in range(pages + 1):
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    print(f"scroll - {page_num}")
    time.sleep(1)
print(f"end scrolling")
end = time.time()
diff = (end - start)


html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
objects = soup.find_all('div', {'class': "flex direction-column flex-1"})

print(f'Time elapsed for {len(objects)} results = {diff} sec')

final_data = []
iter_num = 0
for obj in objects:
    username = obj.text.split('@')[1]
    new_url = partial_url + username
    print(new_url)
    data_dict = {}
    response = requests.get(new_url, headers=headers)
    print(f'Response from the url is: {response.status_code}!')
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    name = soup.find("h1", {"class": "mb-1 color-darker-grey fontSize-24 fontWeight-600 noOfLines-undefined"
                                     " styles_center__giBw7"})
    data_dict['username'] = username
    data_dict['name'] = name
    number = soup.find("div", {"class": "color-lighter-grey fontSize-14 fontWeight-400 noOfLines-undefined "
                                        "styles_center__giBw7"})

    data_dict['number'] = number
    followers = soup.find("div", {"class": "hover-blue color-lighter-grey fontSize-14 fontWeight-400"
                                           " noOfLines-undefined styles_center__giBw7"})

    data_dict['followers'] = followers
    following = soup.find("div", {"class": "hover-blue color-lighter-grey fontSize-14 fontWeight-400 noOfLines-undefined"
                                         " styles_center__giBw7"})

    data_dict['following'] = following
    links = {}
    links = soup.find("div", {"class": "styles_links__VhmRM"})
    desc = links.find_all('a')
    for d in desc:
        if d.has_attr('href'):
            links[d.text] = d['href']

