# -*- coding: utf-8 -*-
# @Time    : 24 1月 2025 6:59 下午
# @Author  : codervibe
# @File    : filterProxies.py
# @Project : vibeProxyPool
# 读取 当前目录上一层目录下的  output 目录下的 proxies.json 文件，并过滤出可用的代理 并将可用的代理输出到文件中

import os
import json
import requests


def is_proxy_available(proxy, proxy_type):
    """
    检查代理是否可用。
    :param proxy: 代理字符串，例如 "http://127.0.0.1:8080"
    :param proxy_type: 代理类型，例如 "HTTP" 或 "HTTPS"
    :return: 如果代理可用，返回 True；否则返回 False
    """
    url = 'https://www.baidu.com/' if proxy_type.upper() == 'HTTPS' else 'http://www.baidu.com/'
    try:
        response = requests.get(url, proxies={proxy_type.lower(): proxy}, timeout=5)
        if response.status_code == 200 and response.json().get('origin') == proxy.split('//')[1]:
            print(f"proxy: {proxy}")
            return True
    except requests.RequestException:
        pass
    return False

def filter_proxies():
    # 获取当前目录的上一层目录
    parent_dir = os.getcwd()
    # print(f"{parent_dir}")
    # 构建 proxies_filter.json 文件的完整路径
    input_file_path = os.path.join(parent_dir, 'output', 'proxies.json')
    # print(f"{input_file_path}")
    # 构建输出文件的完整路径
    output_file_path = os.path.join(parent_dir, 'output', 'proxies_filter.json')

    # 读取 JSON 文件内容
    with open(input_file_path, 'r', encoding='utf-8') as file:
        proxies = json.load(file)

    # 过滤出可用的代理
    available_proxies = []
    for proxy_info in proxies:
        ip = proxy_info.get("IP地址")
        port = proxy_info.get("端口")
        proxy_type = proxy_info.get("类型")
        if ip and port and proxy_type:
            proxy = f"{proxy_type.lower()}://{ip}:{port}"
            if is_proxy_available(proxy, proxy_type):
                available_proxies.append(proxy)

    # 将可用的代理写入新的文件
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(available_proxies, file, ensure_ascii=False, indent=4)

    return available_proxies



