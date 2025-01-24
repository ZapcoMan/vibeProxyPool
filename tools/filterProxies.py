# -*- coding: utf-8 -*-
# @Time    : 24 1月 2025 6:59 下午
# @Author  : codervibe
# @File    : filterProxies.py
# @Project : vibeProxyPool
# 读取 当前目录上一层目录下的  output 目录下的 proxies.json 文件，并过滤出可用的代理 并将可用的代理输出到文件中


if __name__ == "__main__":
    proxies_filter = filter_proxies()
    print(f"可用的代理已保存到 proxies_filter.json 文件中，共 {len(proxies_filter)} 个可用代理")
