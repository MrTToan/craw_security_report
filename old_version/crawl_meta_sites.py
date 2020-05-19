from bs4 import BeautifulSoup
import urllib.request
import re
import pandas as pd
import time

# write HTML to a file in case no Internet available
# with open("meta_page.html", "w", encoding="utf-8") as f:
#     f.write(soup.prettify())

url = (
    "http://congbothongtin.ssc.gov.vn/idsPortal/ttcb/bctc/index.ubck?idBcBaoCao=&ttBc=&"
)
# cpage=2: add this params to the url to navigate to needed pages


def get_last_page(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    filter_div_tag = soup.find_all("div", class_="pager")
    filter_span_tag = filter_div_tag[0].find_all("span", class_="pages")
    last_page = filter_span_tag[0].text.split("/")[-1].strip()
    return last_page


def parse_element_to_table(input, value):
    arr = []
    arr.append(input[value].text.strip())
    return arr


def get_report_id(input, start_point, step):
    report_number = []
    period_number = []
    for i in range(start_point, len(input), step):
        func_name = input[i].a["href"]
        func_value = re.findall(r"\(.*?\)", func_name)
        splitting = func_value[0].split()
        report_number.append(splitting[0][1:-1])
        period_number.append(splitting[1][0:-1])
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
            time.sleep(60)
            if i == 10:
                break
    return page


def crawler(url):
    last_page = get_last_page(url)
    complete_df = []
    # for i in range(int(last_page)):
    for i in range(500):
        page = open_page(url + "cpage=" + str(i))
        soup = BeautifulSoup(page, "html.parser")

        # There are 2 approaches:
        # This paragrahp is the first one which use `tr` tag
        # name = soup.find_all('tr', class_='')
        # t = []
        # for i in name:
        #     h = i.find_all('td')
        #     t.append(h)
        # print(name[8].contents[3].text)
        # print(name[8].contents[5].a['href'])

        # Second approach: use `table` tag
        table = soup.find_all("table", class_="product-table")
        data = table[0].find_all("td")
        # id: need to remove \n \t
        # company name: no need to do
        # report name: need to remove \n \t
        # report_id & period_id: different extraction method
        # quarter name: remove \n \t
        # trich yeu: remove \n \t
        # time sent: remove \n \t
        id = parse_element_to_table(data, 0, 7)
        company_name = parse_element_to_table(data, 1, 7)
        report_name = parse_element_to_table(data, 2, 7)
        quarter_name = parse_element_to_table(data, 3, 7)
        trich_yeu = parse_element_to_table(data, 4, 7)
        time_sent = parse_element_to_table(data, 5, 7)
        report_number, period_number = get_report_id(data, 2, 7)
        dict = {
            "id": id,
            "company_name": company_name,
            "report_name": report_name,
            "report_number": report_number,
            "period_number": period_number,
            "quarter_name": quarter_name,
            "trich_yeu": trich_yeu,
            "time_sent": time_sent,
        }
        df = pd.DataFrame(dict)
        complete_df.append(df)
    final_df = pd.concat(complete_df)
    return final_df


if __name__ == "__main__":
    df = crawler(url)
    print(df.info)
