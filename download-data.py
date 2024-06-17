import requests
from bs4 import BeautifulSoup  
import json
import os


###### Parses HTML content obtained by HTTP GET request to https://celr.dph.ncdhhs.gov/microBiology' to extract list of counties. 
url = 'https://celr.dph.ncdhhs.gov/microBiology'
params = {
    'client.rasclientId': '566000798E',
    'filterBy': '1',
    'recentDay': '5',
    'docFrom': '',
    'docTo': ''
}
response = requests.get(url, params=params, verify=False)
print(response.status_code)
content = BeautifulSoup(response.text, 'html.parser')


##### create a list of all counties and identification number
counties_list = []
values_list = []
for option in content.find_all('option'):
    counties_list.append(option.get_text())
    values_list.append(option.get('value'))
print(values_list)



##### create a mass link of lists for every pdf available for each county
list_of_links = []
for en, id_ in enumerate(values_list):
    # r = requests.get('https://celr.dph.ncdhhs.gov/microBiology?client.rasclientId=' + id +'&filterBy=1&recentDay=5&docFrom=&docTo=',headers={'Connection': 'keep-alive'})
    print(counties_list[en],id_)
    url = 'https://celr.dph.ncdhhs.gov/microBiology'
    params = {
    'client.rasclientId':id_,
    'filterBy': '1',
    'recentDay': '5',
    'docFrom': '',
    'docTo': ''}
    try:
        response = requests.get(url, params=params,verify=False)
        # print(response.text)
        print(response.status_code)
        
        content = BeautifulSoup(response.text, 'html.parser')
        for link in content.find_all('a'):
            list_of_links.append(link['href'])
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



def remove_items(list_, items_remove):
    #####  Removes items/elements that do not link to any pdf
    res = [i for i in list_ if (i not in items_remove)]
    return res
# clean the list of links to retain only valid links
list_of_links = remove_items(list_of_links, ['','index', '#', 'organicChem', 'InOrganicChemistry', 'radioChemistry', 'lead', 'microBiology', 'milk', 'publicWaterSystem', 'rabies'])
print("Sample links: ", list_of_links[:10])
print(len(list_of_links))



##### Downloads PDFs
for en, link in enumerate(list_of_links):
    if(en<10): ###### comment this to download all pdfs
        r = requests.get('https://celr.dph.ncdhhs.gov/' + link, verify= False)
        with open(r'file' + str(en) + '.pdf', "wb") as f: ### Change the folder name 'r'....../file'
            f.write(r.content)

