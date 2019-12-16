from bs4 import BeautifulSoup
from lxml import etree
import requests
import csv
from tqdm import tqdm

headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        }
url_root = 'https://hospitals.webometrics.info/en/world?page='

def store_info_by_page(url):
    #There are 100 hospitals for a specific url .Store them.
    hospitals_list = []
    r = requests.get(url=url, headers=headers)
    r.encoding = ('utf8')
    soup = BeautifulSoup(r.text)
    tbody = soup.find_all("tbody")[0]
    tr_all = tbody.find_all("tr")
    for tr in tr_all:
        dict_tmp = {}
        td_all = tr.find_all("td")
        Ranking = td_all[0].find("center").getText()
        Instituto = td_all[1].find("a").getText()
        Country = td_all[2].find("center").find("img")['src'][-6:-4]
        Size = td_all[3].find("center").getText()
        Visibilidad = td_all[4].find("center").getText()
        Ficheros_ricos = td_all[5].find("center").getText()
        Scholar = td_all[6].find("center").getText()
        dict_tmp['Ranking'] = Ranking
        dict_tmp['Instituto'] = Instituto
        dict_tmp['Country'] = Country
        dict_tmp['Size'] = Size
        dict_tmp['Visibilidad'] = Visibilidad
        dict_tmp['Ficheros_ricos'] = Ficheros_ricos
        dict_tmp['Scholar'] = Scholar
        hospitals_list.append(dict_tmp)
    return hospitals_list

def get_all_info(url_root):
    # get all information
    
    hospitals_list_all = []
    for i in tqdm(range(50)):
        url = url_root + str(i)
        hospitals_list_all+=store_info_by_page(url)
    return hospitals_list_all


def trans_to_csv(hospitals_list_all,out_file):
    #transform the list to csv
    with open(out_file,'w',encoding='utf8') as f:
        w = csv.writer(f)
        filednames = hospitals_list_all[0].keys()
        w.writerow(filednames)
        for row in hospitals_list_all:
            w.writerow(row.values())


hospitals_list_all = get_all_info(url_root)
trans_to_csv(hospitals_list_all,'out.csv')
