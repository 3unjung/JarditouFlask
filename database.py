import mysql.connector


def connexionMysql():
    sqlConnection = mysql.connector.connect(host="localhost", user="root", password="", database="jarditou")
    # cursor.execute("ALTER TABLE test ADD sujet_test int(02);")
    # cursor.execute("ALTER TABLE test DROP squery")
    return sqlConnection
