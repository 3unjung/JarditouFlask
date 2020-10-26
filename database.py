import mysql.connector


def connexionMysql():
    try:
        sqlConnection = mysql.connector.connect(host="localhost", user="root", password="", database="jarditou")
        cursor = sqlConnection.cursor()
        # cursor.execute("ALTER TABLE test ADD sujet_test int(02);")
        # cursor.execute("ALTER TABLE test DROP squery")

    except mysql.connector.Error as error:
        print("Unable to connect to database server")
