# %%
import requests
from bs4 import BeautifulSoup

headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    }

def get_content(url):
    resp = requests.get(url, headers=headers)
    return resp

def get_basic_infos(soup):
    div_page = soup.find("div", class_ = "td-page-content")
    nome = div_page.find_all("p")[0]
    paragrafo = div_page.find_all("p")[1]
    img = nome.find('img')
    nome = img.get('alt', 'default_value')
    ems = paragrafo.find_all("em")
    data = {}
    for i in ems:
        chave, valor, *_ = i.text.split(":")
        chave = chave.strip(" ")
        data[chave]  = valor.strip(" ")
    data["Nome"] = nome
    return data

def get_aparicoes(soup):
    lis = soup.find("div", class_ = "td-page-content").find("h4").find_next().find_all("li")
    aparicoes = [i.text for i in lis]
    aparicoes
    return aparicoes

def get_links():
    url = "https://www.residentevildatabase.com/personagens/"

    resp = requests.get(url, headers=headers)
    soup_personagens = BeautifulSoup(resp.text)
    ancoras = soup_personagens.find("div", class_="td-page-content").find_all("a")
    links = [i["href"] for i in ancoras]
    return links

def get_personagens_infos(url):
    resp = get_content(url)

    if resp.status_code != 200:
        print("Não foi possível obter os dados!")
        return None
    else: 
        soup = BeautifulSoup(resp.text)
        data = get_basic_infos(soup)
        data["Aparicoes"] = get_aparicoes(soup)
        return data

# %%
links = get_links()
data = []
for i in links:
    d = get_personagens_infos(i)
    print(d)
    if d is not None:
        d["link"] = i
        data.append(d)

# %%
data
# %%
