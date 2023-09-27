import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.structures import CaseInsensitiveDict

url = 'https://www.gralon.net/mairies-france/loire-atlantique/' \
      'equipements-sportifs-plateau-eps-multisports-city-stades-44109.htm'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
headers = {'User-Agent': user_agent}
response = requests.get(url, headers=headers)
print(f'Response from the url is: {response.status_code}!')
html = response.text
soup = BeautifulSoup(html, 'html.parser')
list_results = soup.find_all("a", {"class": "booking-item"})

href_links = []

for result in list_results:
    if result.has_attr('href'):
        href_links.append(result['href'])

print(f'There will be performed {len(href_links)} iterations!')

final_data = []
iter_num = 0
for link in href_links:
    iter_num += 1
    data_dict = {}
    link_response = requests.get(link, headers=headers).text
    new_soup = BeautifulSoup(link_response, 'html.parser')
    data_dict['link'] = link
    title = new_soup.find('span', {"class": "fn org"})
    data_dict['title'] = title.text
    address1 = new_soup.find('span', {"class": "street-address"})
    address2 = new_soup.find('span', {"class": "postal-code"})
    address3 = new_soup.find('span', {"class": "locality"})
    address = address1.text + ' ' + address2.text + ' ' + address3.text
    data_dict['address'] = address
    data_dict['description'] = {}
    description_presentation1 = new_soup.find_all('h3')[0]
    data_dict['description']['presentation'] = [description_presentation1.text]
    description_presentation2 = new_soup.find_all('h4')[0]
    data_dict['description']['presentation'].append(description_presentation2.text.replace('\n', ' '))
    description_presentation3 = new_soup.find_all('p')[0]
    data_dict['description']['presentation'].append(description_presentation3.text)
    description_information1 = new_soup.find_all('h3')[1]
    data_dict['description']['information'] = [description_information1.text]
    description_information2 = new_soup.find_all('div', {'class': 'col-md-12'})
    desc = description_information2[1].find_all('li')

    for d in desc:
        data_dict['description']['information'].append(d.text)
    description_equipment1 = new_soup.find_all('h4')[1]
    data_dict['description']['equipments'] = [description_equipment1.text]
    desc2 = description_information2[2].find_all('li')
    if len(desc2) > 0:
        for des in desc2:
            data_dict['description']['information'].append(des.text)
    description_activities1 = new_soup.find_all('h4')[2]
    data_dict['description']['activities'] =[description_activities1.text]

    # description_presentation8 = new_soup.find_all('h4')[3]
    # print(description_presentation8)
    desc3 = description_information2[3].find_all('li')
    for de in desc3:
        data_dict['description']['activities'].append(de.text.replace('\n', ' '))

    url_geoapi = f"https://api.geoapify.com/v1/geocode/search?text={address}&apiKey=09751159bf9740d6a2096e54f0907a01"

    headers1 = CaseInsensitiveDict()
    headers1["Accept"] = "application/json"

    resp = requests.get(url_geoapi, headers=headers1)

    json_object = resp.json()
    lon = json_object['features'][0]['properties']['lon']
    lat = json_object['features'][0]['properties']['lat']

    data_dict['lon'] = lon
    data_dict['lat'] = lat
    final_data.append(data_dict)
    print(f'{iter_num} iteration finished!')


data_frame = pd.DataFrame(final_data)
data_frame.to_csv('web_scraping_data.csv')
print('Finished, you can open the exported csv file in excell')
