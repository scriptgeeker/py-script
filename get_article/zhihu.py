# pip install requests
# pip install bs4
# pip install lxml

import requests
from bs4 import BeautifulSoup

url = input('URL:')

dir = r'C:\Users\BenQ\Downloads'

# 访问伪装
user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/76.0.3809.132 Safari/537.36')

headers = {'User-Agent': user_agent}

# 发送请求
response = requests.get(url, headers=headers)
assert response.status_code == 200

title, label, content = '', '', ''
soup = BeautifulSoup(response.text, 'lxml')

# 获取内容
title += soup.select('h1.QuestionHeader-title')[0].get_text()
label += soup.select('span.AuthorInfo-name')[0].get_text()

for ele in soup.select('div.RichContent-inner')[0].descendants:
    if not hasattr(ele, 'children'):
        if hasattr(ele, 'get_text'):
            content += ele.get_text()
        elif hasattr(ele, 'string'):
            content += ele.string
        content = content + '\n'

# 去除样式
if not label.find('.css') == -1:
    label = label[:label.index('.css')]

# 处理文本
import re

title = re.sub(r'\s', '', title)
label = re.sub(r'\s', '', label)
content = re.sub(r'\s{2,}', '\n', content)

# 创建目录
import os

if not os.path.exists(dir):
    os.makedirs(dir)

file = '{title} - {label}的回答.txt'.format(title=title, label=label)
path = os.path.join(dir, file)

# 写入文件
fw = open(path, 'w', encoding='utf8')
fw.write(content)
fw.close()

print(os.path.abspath(path))
