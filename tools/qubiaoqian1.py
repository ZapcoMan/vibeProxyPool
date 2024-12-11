import re

import requests

from data import canshu


def clean_tag(tag):
    """
    清除标签中的文本，并移除前后空格。

    参数:
    tag: BeautifulSoup Tag对象，需要提取文本的标签。

    返回:
    str: 提取后的文本字符串。
    """
    return tag.get_text(strip=True)


def parse_table(tbody):
    """
    解析表格数据。

    参数:
    tbody: BeautifulSoup Tag对象，需要解析的表格主体。

    返回:
    list: 包含表格数据的二维列表。
    """
    if tbody:
        tbody_rows = [[clean_tag(td) for td in row.find_all("td")] for row in tbody.find_all("tr")]
    else:
        tbody_rows = []

    return tbody_rows


def ihuan_table(tbody):
    """
    解析ihuan表格数据。

    参数:
    tbody: BeautifulSoup Tag对象，需要解析的表格主体。

    返回:
    list: 包含表格数据的二维列表。
    """
    if tbody:
        tbody_rows = [[clean_tag(td) for td in row.find_all("td")] for row in tbody.find_all("tr")]
    else:
        tbody_rows = []

    return tbody_rows


def proxylistplus_table(table):
    """
    解析proxylistplus表格数据。

    参数:
    table: BeautifulSoup Tag对象，需要解析的表格。

    返回:
    list: 包含表格数据的二维列表。
    """
    result_data = []
    tr_tags = table.find_all('tr')
    print(canshu.url4_thead)
    for tr_tag in tr_tags:
        td_tags = tr_tag.find_all('td')
        tbody_rows = [td_tag.text.strip() for td_tag in td_tags]
        if len(tbody_rows) == 8 and tbody_rows[0] == '' and isinstance(tbody_rows[2], str) and tbody_rows[2].isdigit():
            result_data.append(tbody_rows)
            print(tbody_rows)

    return result_data


def ip3366_table(table):
    """
    解析ip3366表格数据。

    参数:
    table: BeautifulSoup Tag对象，需要解析的表格。

    返回:
    list: 包含表格数据的二维列表。
    """
    tbody = table.find("tbody")
    tbody_rows = []
    for row in tbody.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) == 7:
            ip = cols[0].text.strip().replace("IP", "")
            port = cols[1].text.strip().replace("PORT", "")
            anonymity = cols[2].text.strip().replace("匿名度", "")
            proxy_type = cols[3].text.strip().replace("类型", "")
            location = cols[4].text.strip().replace("位置", "")
            response_speed = cols[5].text.strip().replace("响应速度", "")
            last_verified = cols[6].text.strip().replace("录取时间", "")
            tbody_rows.append([ip, port, anonymity, proxy_type, location, response_speed, last_verified])
        print("信息:", canshu.url1_thead)
        for rows in tbody_rows:
            print("内容:", rows)
    return tbody_rows


def openproxy_table(url):
    """
    解析openproxy表格数据。

    参数:
    url: str，需要解析的网页URL。

    返回:
    list: 包含表格数据的列表。
    """
    response = requests.get(url, headers=canshu.url5_headers, timeout=10)
    if response.status_code == 200:
        data = response.text
        pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}:\d+\b'
        ip_port_matches = re.findall(pattern, data)
        for match in ip_port_matches:
            print(match)
    else:
        print('出现异常，状态码：{response.status_code}')
    return []
