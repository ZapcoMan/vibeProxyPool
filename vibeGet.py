import requests
from bs4 import BeautifulSoup
import data.canshu
from data import canshu
from tools.qubiaoqian1 import parse_table,ihuan_table,proxylistplus_table,ip3366_table,openproxy_table
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def zdaye():
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
    try:
        # 发起 GET 请求
        response = requests.get(data.canshu.url4, headers=data.canshu.url1_headers, timeout=10)
        response.raise_for_status()  # 检查 HTTP 状态码
        response.encoding = response.apparent_encoding  # 设置编码

        # 解析 HTML 内容
        soup = BeautifulSoup(response.text, "html.parser")

        tables = proxylistplus_table(soup)

        proxies = []
        for row in tables:
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
        print(f"出现了错误 {e}\n请更换ip或过段时间再重新获取")
        return []

def openproxy():
    try:
        print('http代理如下：')
        tables0 = openproxy_table(data.canshu.url5_http)
        print('socks4代理如下：')
        tables1 = openproxy_table(data.canshu.url5_socks4)
        print('socks5代理如下：')
        tables2 = openproxy_table(data.canshu.url5_socks5)

        proxies = []
        for match in tables0 + tables1 + tables2:
            ip, port = match.split(':')
            proxies.append({
                'IP地址': ip,
                '端口': port,
                '类型': 'socks4' if match in tables1 else 'socks5' if match in tables2 else 'http'
            })

        return proxies

    except requests.exceptions.RequestException as e:
        print(f"出现了错误 {e}\n请更换ip或过段时间再重新获取")
        return []
