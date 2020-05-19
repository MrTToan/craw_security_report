# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags

def remove_whitespace(value):
    return value.strip()

class ScrapyTrialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # id = scrapy.Field(
    #     input_processor= MapCompose(remove_tags, remove_whitespace),
    #     output_processor= TakeFirst()
    # )
    id = scrapy.Field()
    company_name = scrapy.Field()
    report_name = scrapy.Field()
    period_number = scrapy.Field()
    quarter_name = scrapy.Field()
    trich_yeu = scrapy.Field()
    time_sent = scrapy.Field()
    report_number = scrapy.Field()

class CompanyItem(scrapy.Item):
    id = scrapy.Field()
    full_name = scrapy.Field()
    ma_chung_khoan = scrapy.Field()
    san_niem_yet = scrapy.Field()
    ma_so_doanh_nghiep = scrapy.Field()
    ngay_cap = scrapy.Field()
    noi_cap = scrapy.Field()
    