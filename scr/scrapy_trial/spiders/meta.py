# -*- coding: utf-8 -*-
import scrapy
from scrapy_trial.items import ScrapyTrialItem
from scrapy_trial.utils import (
    parse_element_to_table,
    get_last_page,
    get_report_id,
    crawl,
)
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
import pandas as pd


class JokeSpider(scrapy.Spider):
    name = "report"
    allowed_domains = ["congbothongtin.ssc.gov.vn"]
    start_urls = [
        "http://congbothongtin.ssc.gov.vn/idsPortal/ttcb/bctc/index.ubck?idBcBaoCao=&ttBc=&"
    ]
    last_page = get_last_page(
        "http://congbothongtin.ssc.gov.vn/idsPortal/ttcb/bctc/index.ubck?idBcBaoCao=&ttBc=&"
    )
    detail_url = (
        "http://congbothongtin.ssc.gov.vn/idsPortal/ttcb/bctc/chitietbaocao.ubck?"
    )
    next_page = 1
    df = []

    def parse(self, response):
        # print(response)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find_all("table", class_="product-table")
        data = table[0].find_all("td")
        for i in range(0, len(data), 7):
            l = ItemLoader(item=ScrapyTrialItem())
            l.add_value("id", parse_element_to_table(data, i))
            l.add_value("company_name", parse_element_to_table(data, i + 1))
            l.add_value("report_name", parse_element_to_table(data, i + 2))
            l.add_value("report_number", get_report_id(data, i + 2)[0])
            l.add_value("period_number", get_report_id(data, i + 2)[1])
            l.add_value("quarter_name", parse_element_to_table(data, i + 3))
            l.add_value("trich_yeu", parse_element_to_table(data, i + 4))
            l.add_value("time_sent", parse_element_to_table(data, i + 5))
            yield l.load_item()

            meta_dict = dict(l.load_item())
            sub_df = pd.DataFrame(meta_dict)

            report_detail_url = (
                self.detail_url
                + "bcbaocaoid="
                + meta_dict["report_number"][0]
                + "&kyBaoCao="
                + meta_dict["period_number"][0]
            )

            report_detail_bcdkt_sheet = crawl(report_detail_url, 0)
            report_detail_kqkd_sheet = crawl(report_detail_url, 1)
            temp_df = pd.concat(
                [sub_df, report_detail_bcdkt_sheet, report_detail_kqkd_sheet], axis=1
            )
            self.df.append(temp_df)

        final_df = pd.concat(self.df).set_index("id")
        final_df.to_csv("abc.csv")

        # if self.next_page < 2:
        #     self.next_page += 1
        #     next_page_link = self.start_urls[0] + "cpage=" + str(self.next_page)
        #     yield scrapy.Request(url=next_page_link, callback=self.parse)
