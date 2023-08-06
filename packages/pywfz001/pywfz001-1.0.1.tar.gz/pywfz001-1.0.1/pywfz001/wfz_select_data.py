import pymssql
import pandas as pd

def res_to_json(col,res):
    res = [dict(zip(col, item)) for item in res]
    return res

def get_data(sql_str):
    connect = pymssql.connect('123.207.201.140', 'wfz', 'wfz@123456', 'py_test')  # 服务器名,账户,密码,数据库名
    if connect:
        print("连接成功!")
    cursor = connect.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    # sql = "select finterid,fname,fage from t_name"
    cursor.execute(sql_str)
    row = cursor.fetchall()
    cursor.close
    connect.close
    print(row)

    col = ['finterid', 'fname', 'fage']
    dd = res_to_json(col, row)

    return dd



if __name__ == '__main__':
    connect = pymssql.connect('123.207.201.140', 'wfz', 'wfz@123456', 'py_test')  # 服务器名,账户,密码,数据库名
    if connect:
        print("连接成功!")
    cursor = connect.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    sql = "select finterid,fname,fage from t_name"
    cursor.execute(sql)
    row = cursor.fetchall()
    cursor.close
    connect.close
    print(row)

    col = ['finterid','fname','fage']

    # res = [ dict(zip(col,item)) for item in row]
    dd = res_to_json(col,row)

    print(dd)

