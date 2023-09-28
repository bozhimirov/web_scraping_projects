from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
import time
import datetime
from bs4 import BeautifulSoup
import pandas as pd
# from requests.structures import CaseInsensitiveDict


driver = webdriver.Chrome()
initial_url = 'https://www.producthunt.com/search/users?q=users&maker=true'
partial_url = 'https://www.producthunt.com/@'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
                 '(KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
headers = {'User-Agent': user_agent}

driver.get(initial_url)


start = time.time()
pages_test = 0
pages_prod = 29
for page_num in range(pages_test + 1):
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    print(f"scroll - {page_num}")
    time.sleep(3)
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
    iter_num += 1
    username = obj.text.split('@')[-1]
    new_url = partial_url + username
    data_dict = {}

    driver.get(new_url)
    response = requests.get(new_url, headers=headers)
    print(f'Response from the url is: {response.status_code}!')

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    name = soup.find("h1").text

    data_dict['username'] = username
    data_dict['name'] = name
    description = soup.find('div', {'class': 'mb-1 color-lighter-grey fontSize-16 fontWeight-300 noOfLines-undefined styles_center__giBw7'}).text
    data_dict['description'] = description
    number = soup.find_all("div", {'class': 'flex direction-row flex-row-gap-3 flex-row-gap-mobile-5 flex-row-gap-widescreen-5'})
    website_number = number[0].find('div').text
    data_dict['number'] = website_number
    followers_ing = number[0].find_all('a')
    followers = followers_ing[0].text.split(' ')[0]
    following = followers_ing[1].text.split(' ')[0]
    data_dict['followers'] = followers
    data_dict['following'] = following
    links_dict = {}
    links = soup.find("div", {"class": "styles_links__VhmRM"})
    if links:
        links_again = links.find_all('a')
        for link in links_again:
            if link.has_attr('href'):
                links_dict[link.text] = link['href']

    data_dict['links'] = links_dict
    final_data.append(data_dict)
    print(f'{iter_num} iteration finished!')
    time.sleep(1)

data_frame = pd.DataFrame(final_data)
name = f'web_scraping_data_{datetime.date.today()}.csv'
data_frame.to_csv(name)
print('Finished, you can open the exported csv file in excell')
