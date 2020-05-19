from bs4 import BeautifulSoup
import urllib.request

url = "http://congbothongtin.ssc.gov.vn/idsPortal/ttcb/bctc/chitietbaocao.ubck?bcbaocaoid=426801&kyBaoCao=3"

page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, "html.parser")

for i in soup.find_all('td'):
    print(i.contents)
