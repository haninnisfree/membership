import mysql.connector

conn = None

try:
    conn = mysql.connector.Connect(host='localhost',
                                   port=3306,
                                   database='store',
                                   user='huhuhu',
                                   password='huhuhu')
    if conn.is_connected():
        print("연결성공!!")
except mysql.connector.Error as e:
    print(e)
finally:
    if conn is not None and conn.is_connected():
        conn.close()

