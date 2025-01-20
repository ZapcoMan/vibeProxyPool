import argparse
import json
import logging
import os
import re
import subprocess
import sys
from io import StringIO

from vibeGet import zdaye, ihuan, ip3366, proxylistplus, openproxy

# 定义输出目录常量
OUTPUT_DIR = 'output'

# 配置日志记录器，设置日志级别为 INFO，并指定日志格式
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 在模块级别定义 old_stdout
old_stdout = ""


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


def update_repository():
    """
    更新本地仓库到最新版本。

    使用 `git pull` 命令从远程仓库拉取最新的代码，并记录日志。
    如果更新过程中出现错误，记录错误日志。
    """
    try:
        result = subprocess.run(['git', 'pull'], check=True, capture_output=True, text=True)
        logging.info("更新成功: %s", result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error("更新失败: %s", e.stderr)
    except FileNotFoundError:
        logging.error("Git 命令未找到，请确保已安装 Git 并将其添加到系统路径中。")


def main():
    """
    主函数。

    创建命令行参数解析器，解析用户输入的参数，并根据参数执行相应的功能。
    """
    global old_stdout
    parser = argparse.ArgumentParser(
        description="获取代理池ip\nVersion：1.8",
        usage="python run.py [-h] [-z] [-i] [-a] [-pr] [-op] [-O] [-u]"
    )

    # 添加各个参数，每个参数都有特定的功能
    parser.add_argument("-z", "--run-zdaye", action="store_true", dest="run_zdaye",
                        help="使用 zdaye 获取代理池ip(高质量/支持全系统/容易被封ip))")
    parser.add_argument("-i", "--run-ihuan", action="store_true", dest="run_ihuan",
                        help="使用 ihuan 获取代理池ip(高质量/仅支持Windows)")
    parser.add_argument("-ip36", "--run-ip3366", action="store_true", dest="run_ip3366",
                        help="使用ip3366获取代理持池（中质量/支持全系统）")
    parser.add_argument("-pr", "--run-proxylistplus", action="store_true", dest="run_proxylistplus",
                        help="使用 proxylistplus 获取代理池ip（中质量/支持全系统）")
    parser.add_argument("-a", "--run-all", action="store_true", dest="run_all",
                        help="运行所有参数（默认不使用-i参数，如果你是Windows系统，请手动添加-i参数）")
    parser.add_argument("-op", "--run-openproxy", action="store_true", dest="run_openproxy",
                        help="使用 openproxy 源获取socks4代理池（中质量/当前全系统可用）")
    parser.add_argument("-O", "--save-output", action="store_true", dest="save_output",
                        help="将获取到的ip池存放在output目录中的proxies.json文件中")
    parser.add_argument("-u", "--update", action="store_true", dest="update",
                        help="更新本地仓库到最新版本")

    # 解析命令行参数
    args = parser.parse_args()

    # 如果用户请求更新仓库，则调用 update_repository 函数并返回
    if args.update:
        update_repository()
        return

    # 用于记录是否执行了有效参数对应的函数
    func_executed = False

    # 用于捕获终端输出内容的对象
    redirected_output = None
    # 如果用户请求保存输出，则重定向标准输出到一个 StringIO 对象
    if args.save_output:
        old_stdout = sys.stdout
        redirected_output = StringIO()
        sys.stdout = redirected_output

    # 存储所有获取到的代理 IP
    all_proxies = []

    try:
        # 如果用户请求运行所有参数
        if args.run_all:
            func_executed = True
            logging.info('运行所有参数(默认不运行-i，如果你是Windows用户请自行添加-i参数)')
            all_proxies.extend(zdaye())
            if args.run_ihuan:
                all_proxies.extend(ihuan())
            all_proxies.extend(ip3366())
            all_proxies.extend(proxylistplus())
            all_proxies.extend(openproxy())

        # 如果用户请求使用 zdaye 获取代理池
        if args.run_zdaye:
            func_executed = True
            logging.info("使用 zdaye 获取代理池ip中...（此参数及其容易被封IP，少用！）")
            all_proxies.extend(zdaye())

        # 如果用户请求使用 ihuan 获取代理池
        if args.run_ihuan:
            func_executed = True
            logging.info("使用 ihuan 获取代理池ip中...")
            all_proxies.extend(ihuan())

        # 如果用户请求使用 ip3366 获取代理池
        if args.run_ip3366:
            # 标记为已执行函数，用于后续判断是否需要执行其他操作
            func_executed = True
            # 记录日志信息，表明当前正在使用ip3366获取代理池
            logging.info('使用ip3366获取代理池中...')
            # 将ip3366函数返回的代理列表添加到所有代理中
            all_proxies.extend(ip3366())

        # 如果用户请求使用 proxylistplus 获取代理池
        if args.run_proxylistplus:
            func_executed = True
            logging.info('使用 proxylistplus 获取代理池中...')
            all_proxies.extend(proxylistplus())

        # 如果用户请求使用 openproxy 获取代理池
        if args.run_openproxy:
            func_executed = True
            logging.info("使用 openproxy 获取代理池中...")
            all_proxies.extend(openproxy())

        # 如果没有执行任何有效参数对应的函数，打印帮助信息
        if not func_executed:
            parser.print_help()

        # 如果用户请求保存输出
        if args.save_output:
            logging.info("将 获取到的代理地址池 保存到 本地")
            # 如果输出目录不存在，则创建目录
            if not os.path.exists(OUTPUT_DIR):
                os.makedirs(OUTPUT_DIR)
            # 将代理池地址以 JSON 格式保存到文件中
            with open(os.path.join(OUTPUT_DIR, 'proxies.json'), 'w', encoding='utf-8') as f:
                json.dump(all_proxies, f, ensure_ascii=False, indent=4)

    except Exception as e:
        # 记录发生的错误
        logging.error(f"发生错误: {e}")

    finally:
        # 恢复标准输出
        if args.save_output:
            sys.stdout = old_stdout
            if redirected_output:
                redirected_output.close()


if __name__ == "__main__":
    main()
