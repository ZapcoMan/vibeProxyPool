import re
import requests
from data import canshu
import logging

# 配置日志记录器
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def clean_tag(tag):
    """
    清除标签中的文本，并移除前后空格。

    参数:
    tag: BeautifulSoup Tag对象，需要提取文本的标签。

    返回:
    str: 提取后的文本字符串。
    """
    text = tag.get_text(strip=True)
    logging.debug(f"Cleaned tag text: {text}")
    return text


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
        logging.debug(f"Parsed table rows: {tbody_rows}")
    else:
        tbody_rows = []
        logging.debug("No tbody found, returning empty list")

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
        logging.debug(f"Parsed ihuan table rows: {tbody_rows}")
    else:
        tbody_rows = []
        logging.debug("No tbody found for ihuan, returning empty list")

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
    for tr_tag in tr_tags:
        td_tags = tr_tag.find_all('td')
        tbody_rows = [td_tag.text.strip() for td_tag in td_tags]
        if len(tbody_rows) == 8 and tbody_rows[0] == '' and isinstance(tbody_rows[2], str) and tbody_rows[2].isdigit():
            result_data.append(tbody_rows)
            logging.debug(f"Added proxylistplus row: {tbody_rows}")

    logging.debug(f"Final proxylistplus result data: {result_data}")
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
    replacements = {
        "IP": "",
        "PORT": "",
        "匿名度": "",
        "类型": "",
        "位置": "",
        "响应速度": "",
        "录取时间": ""
    }
    for row in tbody.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) == 7:
            row_data = [cols[i].text.strip().replace(key, value) for i, (key, value) in enumerate(replacements.items())]
            tbody_rows.append(row_data)
            logging.debug(f"Added ip3366 row: {row_data}")

    logging.debug(f"Final ip3366 result data: {tbody_rows}")
    return tbody_rows


def openproxy_table(url):
    """
    解析openproxy表格数据。

    参数:
    url: str，需要解析的网页URL。

    返回:
    list: 包含表格数据的列表。
    """
    try:
        # 基本的URL验证
        if not url.startswith("http"):
            raise ValueError("Invalid URL")

        # 发起GET请求并处理响应
        response = requests.get(url, headers=canshu.url5_headers, timeout=10)
        response.raise_for_status()  # 抛出HTTP错误
        data = response.text

        # 使用正则表达式匹配IP:端口模式
        pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}:\d+\b'
        ip_port_matches = re.findall(pattern, data)

        # 记录匹配到的IP:端口信息
        logging.debug(f"Found openproxy IP:Port matches: {ip_port_matches}")

        # 返回匹配到的IP:端口列表
        return ip_port_matches
    except requests.RequestException as e:
        # 处理请求异常
        logging.error(f'请求异常: {e}')
    except ValueError as e:
        # 处理值错误异常
        logging.error(f'值错误: {e}')
    # 如果发生异常，返回空列表
    return []
