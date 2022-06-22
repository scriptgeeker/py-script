'''
Windows 环境下通过 3to2 将
Python 3 代码转为 Python 2 代码
'''

import os

# 查找 Python 安装目录
py_path = None
for env_dir in os.environ['PATH'].split(';'):
    if env_dir.lower().find('python') != -1:
        if os.path.exists(env_dir + '/python.exe'):
            py_path = env_dir
if py_path is None:
    raise Exception('Python program not found')

# 检查是否安装 3to2
if not os.path.exists(py_path + '/Scripts/3to2'):
    # os.system('pip install 3to2')
    raise Exception('3to2 was not installed')

# 获取用户输入的文件路径
file_path = input('Enter file path: ')
file_path = os.path.abspath(file_path)
if not os.path.exists(file_path):
    raise Exception('File does not exist')
if not os.path.isfile(file_path):
    raise Exception('This is not a file')

# 调用 3to2 工具进行转换
fmt = '"%s/python.exe" "%s/Scripts/3to2" -w "%s"'
cmd = fmt % (py_path, py_path, file_path)
tip = os.popen(cmd).read()

# 将生成的文件重命名
dirname = os.path.dirname(file_path)
basename = os.path.basename(file_path)
splitext = os.path.splitext(basename)
# # python 2 文件
src = dirname + '/' + basename
dst = dirname + '/' + (splitext[0] + '-3to2' + splitext[1])
if os.path.exists(dst):
    os.remove(dst)
os.rename(src=src, dst=dst)
# # python 3 文件
src = dirname + '/' + basename + '.bak'
dst = dirname + '/' + (splitext[0] + splitext[1])
if os.path.exists(dst):
    os.remove(dst)
os.rename(src=src, dst=dst)

# 脚本添加文件声明
file_path = dirname + '/' + (splitext[0] + '-3to2' + splitext[1])
with open(file_path, 'r+', encoding='utf8') as frp:
    content = (
            '#!/usr/bin/python2' + '\n'
            + '# -*- coding: UTF-8 -*-' + '\n\n'
            + frp.read()
    )
    frp.seek(0, 0)
    frp.write(content)

print('RefactoringTool:', file_path)
