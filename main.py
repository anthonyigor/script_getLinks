import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
from datetime import datetime
import re


list_links = []
final_list_links = []
dict = {}
list_time = []
final_list_time = []


def getLinks(url,depth, fileName):
    html = requests.get(url)

    #extração dos links
    soup = BeautifulSoup(html.content, 'html.parser')
    found_links = soup.find_all('a', href=re.compile("http"))
    for link in found_links:
        get = link.get('href')
        if get not in list_links:
            list_links.append(get)
            list_time.append(datetime.now().strftime('%d/%m/%Y %H:%M'))

    # percorre cada link da lista e aplica a função getLinks, de acordo com o depth
    if (depth > 0):
        for l in list_links:
            getLinks(l, depth-1, fileName)

    #salva os dados em um dicionário
    for i in range(0, len(list_links)-1):
        final_list_links.insert(i, list_links[i])
        final_list_time.insert(i, list_time[i])
    dict.update({'link': final_list_links, 'atualTime': final_list_time})

    #transforma o dicionário em dataframe e cria arquivo excel
    data_frame = pd.DataFrame(data=dict)
    data_frame.to_excel(f'{fileName}', sheet_name='pagina01', index=False)
    print(f'Procura finalizada! Links disponíveis em {fileName}')

url = input('Informe a URL desejada: ')
depth = int(input('Profundidade da procura: '))
fileName = input('Nome do arquivo final [.xlsx]: ')
getLinks(url, depth, fileName)
