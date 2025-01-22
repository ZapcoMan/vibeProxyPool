import logging
import re

import requests

from data import canshu

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
    # 初始化结果列表，用于存储满足条件的行数据
    result_data = []

    # 查找表格中所有的<tr>标签
    tr_tags = table.find_all('tr')

    # 遍历每一个<tr>标签
    for tr_tag in tr_tags:
        # 查找当前<tr>标签下的所有<td>标签
        td_tags = tr_tag.find_all('td')

        # 提取<td>标签中的文本内容，并去除前后空格
        tbody_rows = [td_tag.text.strip() for td_tag in td_tags]

        # 检查提取的行数据是否满足特定条件：共有8列，第一列为空，第三列是数字类型的字符串
        if len(tbody_rows) == 8 and tbody_rows[0] == '' and isinstance(tbody_rows[2], str) and tbody_rows[2].isdigit():
            # 如果满足条件，则将该行数据添加到结果列表中，并记录日志
            result_data.append(tbody_rows)
            logging.debug(f"Added proxylistplus row: {tbody_rows}")

    # 输出最终的结果列表，并返回
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
    # 遍历tbody下的所有<tr>元素

    for row in tbody.find_all("tr"):
        # 获取当前<tr>元素下的所有<td>元素
        cols = row.find_all("td")
        # 检查列的数量是否为7，以确保数据结构正确
        if len(cols) == 7:
            # 构造行数据列表，替换特定关键词为其对应值
            row_data = [cols[i].text.strip().replace(key, value) for i, (key, value) in enumerate(replacements.items())]
            # 将处理后的行数据添加到tbody_rows列表中
            tbody_rows.append(row_data)
            # 记录添加的行数据
            logging.debug(f"Added ip3366 row: {row_data}")

    # 记录最终处理后的数据列表
    logging.debug(f"Final ip3366 result data: {tbody_rows}")
    # 返回处理后的数据列表
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
