# -*- coding: utf-8 -*-
import scrapy
# from scrapy_trial.items import DetailItem
from scrapy_trial.utils import parse_element_to_table, get_last_page, get_report_id
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
import pandas as pd

class ReportDetailSpider(scrapy.Spider):
    name = "report_detail"
    allowed_domains = ["congbothongtin.ssc.gov.vn"]
    start_urls = [
        "http://congbothongtin.ssc.gov.vn/idsPortal/ttcb/bctc/chitietbaocao.ubck?"
    ]
    next_page = 1
    df = []

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find_all("table", class_="product-table")
        data = table[0].find_all("td")
        for i in range(0, len(data), 7):
            l = ItemLoader(item=DetailItem())
            l.add_value("id", parse_element_to_table(data, i))
            l.add_value("full_name", parse_element_to_table(data, i + 1))
            l.add_value("ma_chung_khoan", parse_element_to_table(data, i + 2))
            l.add_value("san_niem_yet", parse_element_to_table(data, i + 3))
            l.add_value("ma_so_doanh_nghiep", parse_element_to_table(data, i + 4))
            l.add_value("ngay_cap", parse_element_to_table(data, i + 5))
            l.add_value("noi_cap", parse_element_to_table(data, i + 6))
            yield l.load_item()
            sub_df = pd.DataFrame(dict(l.load_item()))
            self.df.append(sub_df)
        final_df = pd.concat(self.df).set_index('id')

        if self.next_page < int(last_page):
            self.next_page += 1
            # next_page_link = self.start_urls[0] + "bcbaocaoid=" + ??? + "&kyBaoCao" + ??? + "#" + ???
            yield scrapy.Request(url=next_page_link, callback=self.parse)
