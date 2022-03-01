#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os

# MYSQL 环境变量路径
PATH = r'C:\Program Files\MySQL\MySQL Server 5.7\bin'

# 数据库连接信息
HOST = r'127.0.0.1'  # 地址
PORT = r'3306'  # 端口号
USER = r'root'  # 用户名
PSWD = r'root'  # 密码


# 生成连接数据库字符串
def get_connect_str(host, port, user, pswd):
    fmt = '-h{host} -P{port} -u{user} -p{pswd}'
    cli = fmt.format(host=host, port=port, user=user, pswd=pswd)
    return ' ' + cli + ' '


# 获取数据库列表
def get_database_list(bin_path, conn_str):
    fmt = '"{path}/mysql" {conn} -e "show databases"'
    cli = fmt.format(path=bin_path, conn=conn_str)
    text = os.popen(cli).read().strip()
    db_list = text.split('\n')[1:]
    return db_list


# 获取数据库中表
def get_table_list(bin_path, conn_str, db_name):
    fmt = '"{path}/mysql" {conn} -e "show tables from {name}"'
    cli = fmt.format(path=bin_path, conn=conn_str, name=db_name)
    text = os.popen(cli).read().strip()
    tb_list = text.split('\n')[1:]
    return tb_list


# 导出数据库到文件
def export_sql_file(bin_path, conn_str, db_name):
    fmt = '"{path}/mysqldump" {conn} {name} > {name}.sql'
    cli = fmt.format(path=bin_path, conn=conn_str, name=db_name)
    if os.system(cli) == 0:
        sql_file = os.path.abspath(db_name + '.sql')
        if os.path.getsize(sql_file) != 0:
            return sql_file
    return None


# 从文件中导入数据
def import_sql_data(bin_path, conn_str, sql_file):
    fmt = '"{path}/mysql" {conn} {name} < {file}'
    db_name = os.path.splitext(os.path.basename(sql_file))[0]
    cli = fmt.format(path=bin_path, conn=conn_str, name=db_name, file=sql_file)
    if os.system(cli) == 0:
        tb_list = get_table_list(bin_path, conn_str, db_name)
        if len(tb_list) != 0:
            return tb_list
    return None


if __name__ == '__main__':
    bin_path = os.path.abspath(PATH)
    conn_str = get_connect_str(HOST, PORT, USER, PSWD)

    # 导入/导出操作提示
    print('数据库导入/导出脚本：')
    print('\t1、导出数据库到文件')
    print('\t2、从文件中导入数据')
    opt = input('请输入操作序号：')

    # 1、导出数据库到文件
    if opt == '1':
        db_list = get_database_list(bin_path, conn_str)
        for item in db_list:
            print('\t*', item)
        db_name = input('请输入数据库名称：')
        sql_file = export_sql_file(bin_path, conn_str, db_name)
        if sql_file is not None:
            print('数据转储SQL文件成功！')
            print(sql_file)
        else:
            print('数据转储失败，请检查：')
            print('\t1、数据库名称是否输入正确')
            print('\t2、文件是否被其他程序占用')

    # 2、从文件中导入数据
    if opt == '2':
        path = input('请输入SQL文件路径：')
        sql_file = os.path.abspath(path)
        tb_list = import_sql_data(bin_path, conn_str, sql_file)
        if tb_list is not None:
            print('数据导入数据库成功！')
            print(tb_list)
        else:
            print('数据导入失败，请检查：')
            print('\t1、文件名是否与数据库名一致')
            print('\t2、文件所在路径是否拼写正确')
