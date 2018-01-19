import certifi
import urllib3
import json
from bs4 import BeautifulSoup

base_url = "https://www.sahibinden.com"
user_input = input("Adres girin : ").split('/')[-1]
data = []
unvisited = []
unvisited.append(user_input)


def page_crawler(page_url, data):
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    r = http.request('GET', page_url)
    page = r.data

    soup = BeautifulSoup(page, 'html.parser')
    nextButton = soup.find_all('a', {"class" : "prevNextBut"})[-1]['href']
    clear_text = '&query_text'
    if clear_text in nextButton:
        nextButton = nextButton[:nextButton.index(clear_text)]
    rows = soup.find_all('tr', {"class": "searchResultsItem"})
    for row in rows:
        cols = []
        item = row.find('td', {"class" : "searchResultsTagAttributeValue"})
        if item == None:
            continue

        # Append main elements (Tag, link, Price, Date, Location) to col[]
        cols.append(item.string.strip())
        cols.append(row.find('a', {"class" : "classifiedTitle"})['href'])
        cols.append(row.find('td', {"class" : "searchResultsPriceValue"}).find('div').string)
        cols.append(row.find('td', {"class" : "searchResultsDateValue"}).find('span').string)
        cols.append(row.find('td', {"class" : "searchResultsLocationValue"}).text.strip())

        # Append remaining elements
        for ele in row.find_all('td', {"class" : "searchResultsAttributeValue"}):
            cols.append(ele.text.strip())

        data.append(cols)

    return 0


def paging(page_url):
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    r = http.request('GET', page_url)
    page = r.data

    
    soup = BeautifulSoup(page, 'html.parser')
    try:
        next_page = soup.find('ul', {"class": "pageNaviButtons"}).find('span', {"class" : "pager-arrow last"}).parent['href']
    except:
        return None
    
    return next_page
i = 0
temp = user_input
while True:
    print("retrieving page : ", i)
    i += 1
    temp = paging(base_url + '/' + temp)
    if temp in unvisited:
        break
    if temp == None:
        break

    unvisited.append(temp)

print(unvisited)
for p in unvisited:
    page_crawler(base_url + '/' +p, data)
