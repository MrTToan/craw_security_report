# a = [1, 2, 3]
# x = range(a[0], len(a), 2)
# for n in x:
#     print(n)

from bs4 import BeautifulSoup
import urllib.request
import re
import pandas as pd
import time
from urllib.error import URLError, HTTPError

# url = (
#     "http://congbothongtin.ssc.gov.vn/idsPortal/ttcb/bctc/index.ubck?idBcBaoCao=&ttBc=&"
# )
# page = urllib.request.urlopen(url)
# soup = BeautifulSoup(page, "html.parser")
# k = soup.find_all('div', class_='pager')
# r = k[0].find_all('span', class_='pages')
# h = r[0].text.split('/')[-1]
# print(h)
# print(k[0].prettify())
url = ('https://tiki.vn/')

code = True
i = 0
while code:   
    try:
        page = urllib.request.urlopen(url)
        code = False
    except HTTPError as e:
        i += 1
        print(f'Lan thu: {i}')
        time.sleep(5)
        if i == 3:
            break;