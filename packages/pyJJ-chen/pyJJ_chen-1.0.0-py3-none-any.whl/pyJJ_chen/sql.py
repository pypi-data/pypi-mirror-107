import pymssql



def do_sql(sql):
    connect = pymssql.connect('123.207.201.140', 'wfz', 'wfz@123456', 'py_test')  # 服务器名,账户,密码,数据库名
    if connect:
        print("连接成功!")
    cursor = connect.cursor()   #创建一个游标对象,python里的sql语句都要通过cursor来执行
    #1 插入数据表
    sql = "select finterid ,fname, fage   from t_name  order by finterid"
    cursor.execute(sql)  # 执行sql语句
    row = cursor.fetchall()  # 读取查询结果,
    return(row)

if __name__ == '__main__':
    sql = "select finterid ,fname, fage   from t_name  order by finterid"
    data=do_sql(sql)
    print(data)
