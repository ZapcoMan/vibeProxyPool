import argparse
from vibeGet import zdaye, ihuan, ip3366, proxylistplus, openproxy
import sys
from io import StringIO
import re
import json
import os

# 定义输出目录常量
OUTPUT_DIR = 'output'


def filter_braces(output):
    """
    过滤大括号中的内容。

    使用正则表达式匹配 {} 中的内容，并返回匹配结果的字符串。

    参数:
    - output: 字符串，包含 {} 的文本。

    返回值:
    - 匹配结果的字符串。
    """
    pattern = r'\[([^}]*)\]'
    matches = re.findall(pattern, output)
    return '\n'.join(matches)


def main():
    """
    主函数。

    创建命令行参数解析器，解析用户输入的参数，并根据参数执行相应的功能。
    """
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(
        description="杨CC-获取代理池ip\nVersion：0.4",
        usage="python run.py [-h] [-z] [-i] [-a] [-pr] [-op] [-O]"
    )
    # 添加各个参数，这里补充上 -O 参数的定义
    parser.add_argument("-z", "--run-zdaye", action="store_true", dest="run_zdaye",
                        help="使用 zdaye 获取代理池ip(高质量/支持全系统/容易被封ip))")
    parser.add_argument("-i", "--run-ihuan", action="store_true", dest="run_ihuan",
                        help="使用 ihuan 获取代理池ip(高质量/仅支持Windows)")
    parser.add_argument("-ip36", "--run-ip3366", action="store_true", dest="run_ip3366",
                        help="使用ip3366获取代理持池（中质量/支持全系统）")
    parser.add_argument("-pr", "--run-proxylistplus", action="store_true", dest="run_proxylistplus",
                        help="使用 proxylistpus 获取代理池ip（中质量/支持全系统）")
    parser.add_argument("-a", "--run-all", action="store_true", dest="run_all",
                        help="运行所有参数（默认不使用-i参数，如果你是Widnows系统，请手动添加-i参数）")
    parser.add_argument("-op", "--run-openproxy", action="store_true", dest="run_openproxy",
                        help="使用 openproxy 源获取socks4代理池（中质量/当前全系统可用）")
    parser.add_argument("-O", "--save-output", action="store_true", dest="save_output",
                        help="将获取到的ip池存放在output目录中的svae.txt文件中")

    # 解析命令行参数
    args = parser.parse_args()

    # 用于记录是否执行了有效参数对应的函数
    func_executed = False
    # 用于捕获终端输出内容的对象
    redirected_output = None
    if args.save_output:
        old_stdout = sys.stdout
        redirected_output = StringIO()
        sys.stdout = redirected_output

    all_proxies = []
    if args.run_all:
        func_executed = True
        print('运行所有参数(默认不运行-i，如果你是Windows用户请自行添加-i参数)')
        all_proxies.extend(zdaye())
        if args.run_ihuan:
            all_proxies.extend(ihuan())
        all_proxies.extend(ip3366())
        all_proxies.extend(proxylistplus())
        all_proxies.extend(openproxy())
    if args.run_zdaye:
        func_executed = True
        print("使用 zdaye 获取代理池ip中...（此参数及其容易被封IP，少用！）")
        all_proxies.extend(zdaye())
    if args.run_ihuan:
        func_executed = True
        print("使用 ihuan 获取代理池ip中...")
        all_proxies.extend(ihuan())
    if args.run_ip3366:
        func_executed = True
        print('使用ip3366获取代理池中...')
        all_proxies.extend(ip3366())
    if args.run_proxylistplus:
        func_executed = True
        print('使用 proxylistplu 获取代理池中...')
        all_proxies.extend(proxylistplus())
    if args.run_openproxy:
        func_executed = True
        print("使用 openproxy 获取代理池中...")
        all_proxies.extend(openproxy())

    if not func_executed:
        parser.print_help()

    if args.save_output:
        print("将 获取到的代理地址池 保存到 本地")
        # 将代理池地址以 JSON 格式保存到文件中
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        with open(os.path.join(OUTPUT_DIR, 'proxies.json'), 'w', encoding='utf-8') as f:
            json.dump(all_proxies, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
