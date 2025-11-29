import base64

def encrypt_url(url):
    """
    简单加密URL
    :param url: 原始URL
    :return: 加密后的URL
    """
    # 使用base64编码URL
    encoded_bytes = base64.b64encode(url.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def decrypt_url(encrypted_url):
    """
    解密URL
    :param encrypted_url: 加密的URL
    :return: 解密后的原始URL
    """
    # 使用base64解码URL
    decoded_bytes = base64.b64decode(encrypted_url.encode('utf-8'))
    return decoded_bytes.decode('utf-8')