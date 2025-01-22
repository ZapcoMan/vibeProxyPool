import requests
from bs4 import BeautifulSoup
import data.canshu
from data import canshu
from tools.qubiaoqian1 import parse_table,ihuan_table,proxylistplus_table,ip3366_table,openproxy_table
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
def zdaye():
    """
    从指定的 URL 中获取代理信息。

    本函数通过发起 HTTP GET 请求，获取网页内容，并解析出代理信息。
    它使用了 requests 库来发起网络请求，BeautifulSoup 库来解析 HTML 内容。
    """
    try:
        # 发起 GET 请求
        response = requests.get(data.canshu.url1, headers=data.canshu.url1_headers, timeout=10)
        response.raise_for_status()  # 检查 HTTP 状态码
        response.encoding = response.apparent_encoding

        # 解析 HTML 内容
        soup = BeautifulSoup(response.text, "html.parser")

        # 获取 tbody 标签
        tbody = soup.find("tbody")

        # 使用 parse_table 函数解析表格
        tbody_rows = parse_table(tbody)

        # 打印表头和内容
        print("信息:", data.canshu.url1_thead)
        proxies = []
        for row in tbody_rows:
            print("内容:", row)
            proxies.append({
                'IP地址': row[0],
                '端口': row[1],
                '类型': row[2],
                '地理位置': row[3],
                '上次验证': row[4],
                'https': row[5],
                'post': row[6],
                '响应时间': row[7],
                '已存活时间': row[8]
            })

        return proxies

    except requests.exceptions.RequestException as e:
        print(f"出现了错误 {e}\n请更换ip或过段时间再重新获取")
        return []


def ihuan():
    """
    从指定的URL中提取代理IP信息，并使用Selenium和BeautifulSoup进行页面加载和数据解析。
    :return: 包含代理IP信息的列表，每个元素是一个包含IP信息的字典。
    """
    try:
        # 设置Chrome选项
        chrome_options = Options()
        chrome_options.add_argument('--headless')

        # 使用Service指定chromedriver路径
        service = Service(canshu.driver_path)

        # 创建webdriver实例
        driver = webdriver.Chrome(service=service, options=chrome_options)
        # 打开页面
        driver.get(canshu.url2)

        # 等待页面加载完成
        driver.implicitly_wait(10)  # 最多等待10秒

        # 获取网页内容
        html = driver.page_source

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html, 'html.parser')

        # 找到表格
        table = soup.find('table', {'class': 'table table-hover table-bordered'})

        # 如果table对象存在，则对其进行处理
        if table:
            # 提取表格中的每一行数据
            rows = table.find_all('tr')[1:]  # 跳过表头

            data = []
            for row in rows:
                cols = row.find_all('td')
                ip_address = cols[0].get_text(strip=True)  # IP地址
                port = cols[1].get_text(strip=True)  # 端口
                location = cols[2].get_text(strip=True)  # 地理位置
                isp = cols[3].get_text(strip=True)  # 运营商
                https = cols[4].get_text(strip=True)  # HTTPS
                post = cols[5].get_text(strip=True)  # POST
                anonymity = cols[6].get_text(strip=True)  # 匿名度
                speed = cols[7].get_text(strip=True)  # 访问速度
                entry_time = cols[8].get_text(strip=True)  # 入库时间
                last_check = cols[9].get_text(strip=True)  # 最后检测

                # 将每一行的数据保存为一个字典
                data.append({
                    'IP地址': ip_address,
                    '端口': port,
                    '位置': location,
                    'HTTPS': https,
                    'POST': post,
                    '访问速度': speed,
                    '入库时间': entry_time,
                    '最后在线时间': last_check
                })

            # 输出提取的结果
            for entry in data:
                print(entry)

            return data

    except requests.exceptions.RequestException as e:
        print(f"出现了错误 {e}\n请更换ip或过段时间再重新获取")
        return []

def ip3366():
    """
    从指定的URL中提取代理IP信息，并使用requests和BeautifulSoup进行数据请求和解析。
    :return: 包含代理IP信息的列表，每个元素是一个包含IP信息的字典。
    """
    try:
        # 发起 GET 请求
        response = requests.get(data.canshu.url3, headers=data.canshu.url1_headers, timeout=10)
        response.raise_for_status()  # 检查 HTTP 状态码
        response.encoding = response.apparent_encoding  # 设置编码

        # 解析 HTML 内容
        soup = BeautifulSoup(response.text, "html.parser")

        tables = ip3366_table(soup)

        proxies = []
        for row in tables:
            proxies.append({
                'IP地址': row[0],
                '端口': row[1],
                '匿名度': row[2],
                '类型': row[3],
                '地理位置': row[4],
                '响应速度': row[5],
                '已存活时间': row[6]
            })

        return proxies

    except requests.exceptions.RequestException as e:
        print(f"出现了错误 {e}\n请更换ip或过段时间再重新获取")
        return []


def proxylistplus():
    """
    从指定的URL获取代理列表。

    本函数通过发起HTTP GET请求，获取HTML内容，并从中解析出代理信息。
    解析成功后，将代理信息以字典列表的形式返回。

    Returns:
        list: 包含代理信息的字典列表，如果请求失败或解析错误，返回空列表。
    """
    try:
        # 发起 GET 请求
        response = requests.get(data.canshu.url4, headers=data.canshu.url1_headers, timeout=10)
        response.raise_for_status()  # 检查 HTTP 状态码
        response.encoding = response.apparent_encoding  # 设置编码

        # 解析 HTML 内容
        soup = BeautifulSoup(response.text, "html.parser")

        # 提取表格数据
        tables = proxylistplus_table(soup)

        proxies = []
        for row in tables:
            # 将每一行数据转换为字典，并添加到代理列表中
            proxies.append({
                '图标': row[0],
                'IP 地址': row[1],
                '端口': row[2],
                '类型': row[3],
                '国家': row[4],
                '谷歌': row[5],
                'Https': row[6]
            })

        return proxies

    except requests.exceptions.RequestException as e:
        # 处理请求异常
        print(f"出现了错误 {e}\n请更换ip或过段时间再重新获取")
        return []


def openproxy():
    """
    获取并打印代理服务器列表。

    本函数尝试从预定义的URL中获取http、socks4和socks5代理服务器列表，
    并以人类可读的格式打印出来。每个代理服务器的信息包括IP地址、端口和类型。

    返回:
        list: 包含所有找到的代理服务器信息的列表，每个元素都是一个字典，
              包括'IP地址'、'端口'和'类型'。
    """
    try:
        # 打印http代理列表
        print('http代理如下：')
        tables0 = openproxy_table(data.canshu.url5_http)
        # 打印socks4代理列表
        print('socks4代理如下：')
        tables1 = openproxy_table(data.canshu.url5_socks4)
        # 打印socks5代理列表
        print('socks5代理如下：')
        tables2 = openproxy_table(data.canshu.url5_socks5)

        # 初始化代理列表
        proxies = []
        # 遍历所有代理服务器并提取信息
        for match in tables0 + tables1 + tables2:
            ip, port = match.split(':')
            # 根据代理类型添加到列表中
            proxies.append({
                'IP地址': ip,
                '端口': port,
                '类型': 'socks4' if match in tables1 else 'socks5' if match in tables2 else 'http'
            })

        # 返回所有代理信息
        return proxies

    except requests.exceptions.RequestException as e:
        # 出现网络请求错误时的处理
        print(f"出现了错误 {e}\n请更换ip或过段时间再重新获取")
        # 错误情况下返回空列表
        return []
