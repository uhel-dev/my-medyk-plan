import mysql.connector


def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='my_medyk_plan'
    )
    return connection
