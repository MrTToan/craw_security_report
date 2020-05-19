from bs4 import BeautifulSoup
import urllib.request
import re
import pandas as pd
import time
import crawl_meta_sites as cms

url = "http://congbothongtin.ssc.gov.vn/idsPortal/ttcb/bctc/chitietbaocao.ubck?"
# bcbaocaoid=433743&kyBaoCao=3#BCDKT

def crawler(url):
    report_type = ['BCDKT', 'KQKD']
    # , 'LCTT-TT', 'LCTT-GT': users don't need
    big_report = []
    for type in report_type:
        report_id = ???
        report_period = ???
        full_url = url + 'bcbaocaoid=' + report_id + 'kyBaoCao=' + report_period + '#' + type


        page = cms.open_page(full_url)
        soup = BeautifulSoup(page, "html.parser")
        table = soup.find_all("table", class_="product-table")
        data = table[0].find_all("td")

        if type == 'BCDKT':
            asset = cms.parse_element_to_table(data, 0, 5)
            # ma_so = cms.parse_element_to_table(data, 1, 5)
            # thuyet_minh = cms.parse_element_to_table(data, 2, 5)
            so_cuoi_ky = cms.parse_element_to_table(data, 3, 5)
            # so_dau_ky = cms.parse_element_to_table(data, 4, 5)

            dict = {
                "tai_san": asset,
                # "ma_so": ma_so,
                # "thuyet_minh": thuyet_minh,
                "so_cuoi_ky": so_cuoi_ky,
                # "so_dau_ky": so_dau_ky,
            }
            df_bcdkt = pd.DataFrame(dict)
            big_report.append(df_bcdkt)
        else:
            chi_tieu= cms.parse_element_to_table(data, 0, 7)
            ki_nay_nam_nay = cms.parse_element_to_table(data, 3, 7)
            
            dict = {
                "chi_tieu": chi_tieu,
                "ki_nay_nam_nay": ki_nay_nam_nay,
            }
            df_kqkd = pd.DataFrame(dict)
            big_report.append(df_kqkd)
    return big_report

