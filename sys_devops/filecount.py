#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys
import time


def walk(path):
    path = os.path.abspath(path)
    global count
    count = 0
    global begin
    begin = time.time()

    # 递归遍历文件目录
    def func(path):
        for dir in os.listdir(path):
            p = os.path.join(path, dir)
            if not os.path.isdir(p):
                global count
                count += 1
            else:
                # log(p)
                func(p)

    # 打印执行日志
    def log(p):
        print(round(time.time(), 3), end='\t')
        print(os.path.basename(p), end='\t')
        print(count)

    func(path)
    print(os.path.basename(path), '目录下文件总数', count)
    print("程序执行时间", round((time.time() - begin), 3), 's')


if __name__ == '__main__':
    path = './'  # 默认当前目录
    if len(sys.argv) > 1:
        path = sys.argv[1]
    walk(path)
