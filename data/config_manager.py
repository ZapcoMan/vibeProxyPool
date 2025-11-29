import configparser
import os
from data.encryption_utils import decrypt_url

# 配置文件路径
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.ini')

def load_config():
    """
    加载配置文件
    :return: 配置解析器对象
    """
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding='utf-8')
    return config

def get_decrypted_url(section, key):
    """
    从配置文件中获取解密后的URL
    :param section: 配置节名
    :param key: 配置键名
    :return: 解密后的URL
    """
    config = load_config()
    encrypted_url = config.get(section, key)
    return decrypt_url(encrypted_url)