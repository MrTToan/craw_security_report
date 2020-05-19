from bs4 import BeautifulSoup
import urllib.request
import re
import pandas as pd
import time
from scrapy.spidermiddlewares.httperror import HttpError
from urllib.error import URLError, HTTPError


def parse_element_to_table(input, value):
    return input[value].text.strip()


def get_last_page(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    filter_div_tag = soup.find_all("div", class_="pager")
    filter_span_tag = filter_div_tag[0].find_all("span", class_="pages")
    last_page = filter_span_tag[0].text.split("/")[-1].strip()
    return last_page


def get_report_id(input, order_in_response):
    func_name = input[order_in_response].a["href"]
    func_value = re.findall(r"\(.*?\)", func_name)
    splitting = func_value[0].split()
    report_number = splitting[0][1:-1]
    period_number = splitting[1][0:-1]
    return report_number, period_number


def open_page(url):
    code = True
    i = 0
    while code:
        try:
            page = urllib.request.urlopen(url)
            code = False
        except HTTPError as e:
            i += 1
            print(f"Lan thu: {i}")
            time.sleep(15)
            if i == 10:
                break
    return page


def crawl(url, report_type):
    page = open_page(url)
    soup = BeautifulSoup(page, "html.parser")
    table = soup.find_all("table", class_="product-table")
    data = table[report_type].find_all("td")
    # print(len(data))
    raw_df = {}
    if len(data) % 5 == 0:
        for i in range(0, len(data), 5):
            name = parse_element_to_table(data, i)
            value = parse_element_to_table(data, i + 3)
            raw_df[name] = value
        df = pd.Series(raw_df).to_frame()
    else:
        for i in range(0, len(data), 7):
            name = parse_element_to_table(data, i)
            value = parse_element_to_table(data, i + 3)
            raw_df[name] = value
    df = pd.Series(raw_df).to_frame()
    return df.T


# test = open_page(
#     "http://congbothongtin.ssc.gov.vn/idsPortal/ttcb/bctc/chitietbaocao.ubck?bcbaocaoid=437101&kyBaoCao=1"
# )

# print(test.read())

# a = crawl(
#     "http://congbothongtin.ssc.gov.vn/idsPortal/ttcb/bctc/chitietbaocao.ubck?bcbaocaoid=437101&kyBaoCao=1",
#     1,
# )
# print(a)
