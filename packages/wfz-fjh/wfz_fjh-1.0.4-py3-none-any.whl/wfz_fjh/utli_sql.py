import pymssql


def sql_select(sql):
    connect = pymssql.connect('123.207.201.140', 'wfz', 'wfz@123456', 'py_test')  # 服务器名,账户,密码,数据库名
    if connect:
        print("连接成功!")
    cursor = connect.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    # 1 插入数据表
    cursor.execute(sql)  # 执行sql语句
    row = cursor.fetchall()  # 读取查询结果,
    cursor.close()  # 关闭游标
    connect.close()  # 关闭连接
    return row


if __name__ == '__main__':
    sql = "select * from t_name"
    row = sql_select(sql)
    print(row)