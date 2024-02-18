import requests
from bs4 import BeautifulSoup
import os

def download_js_files(url):
    # 发送HTTP GET请求获取网页内容
    response = requests.get(url)
    # 使用BeautifulSoup解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到所有的<script>标签
    script_tags = soup.find_all('script')

    for script in script_tags:
        # 尝试获取JavaScript文件的URL
        src = script.get('src')
        if src:
            # 处理可能的相对URL 
            js_url = src if src.startswith('http') else f'{url}{src}'
            try:
                js_response = requests.get(js_url)
                # 获取文件名
                file_name = js_url.split('/')[-1]
                # 确保本地有一个名为js_files的文件夹
                if not os.path.exists('js_files'):
                    os.makedirs('js_files')
                # 将内容写入文件
                with open(f'js_files/{file_name}', 'wb') as file:
                    file.write(js_response.content)
                print(f'Downloaded: {file_name}')
            except requests.exceptions.RequestException as e:
                print(f'Failed to download {js_url}: {e}')

if __name__ == '__main__':
    url = 'http://example.com'  # 更改为你想下载JS文件的网页地址
    download_js_files(url)
