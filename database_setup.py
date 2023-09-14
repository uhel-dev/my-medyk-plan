import hashlib

import mysql.connector
from mysql.connector import errorcode

config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'my_medyk_plan',
    'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# CREATE TABLES

# TABLES = {}
# TABLES['users'] = (
#     "CREATE TABLE IF NOT EXISTS `users` ("
#     "  `id` INTEGER AUTO_INCREMENT PRIMARY KEY,"
#     "  `full_name` varchar(255) NOT NULL,"
#     "  `email` varchar(255) NOT NULL,"
#     "  `password` varchar(255) NOT NULL,"
#     "  `role` enum('ADMIN','USER') NOT NULL"
#     ")")
#
#
# for table_name in TABLES:
#     table_description = TABLES[table_name]
#     try:
#         print("Creating table {}: ".format(table_name), end='')
#         cursor.execute(table_description)
#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
#             print("already exists.")
#         else:
#             print(err.msg)
#     else:
#         print("OK")


# ROOT ADMIN

root_full_name = "Jakub U"
root_password = hashlib.sha256("example".encode()).hexdigest()
root_email = "root@mmp.co.uk"
root_role = 'ADMIN'

try:
    cursor.execute("INSERT INTO users (full_name, email, password, role) VALUES (%s, %s, %s, %s)",
                   (root_full_name, root_email, root_password, root_role))
    cnx.commit()  # Don't forget to commit the changes.
except mysql.connector.Error as err:
    print(f"Error: {err}")

# USERS

username_1_full_name = "Robert M"
username_1_password = hashlib.sha256("username_1_password".encode()).hexdigest()
username_1_email = "robert@mmp.co.uk"
username_1_role = "USER"

try:
    cursor.execute("INSERT INTO users (full_name, email, password, role) VALUES (%s, %s, %s, %s)",
                   (username_1_full_name, username_1_email, username_1_password, username_1_role))
    cnx.commit()  # Don't forget to commit the changes.
except mysql.connector.Error as err:
    print(f"Error: {err}")

username_2_full_name = "Pawel K"
username_2_password = hashlib.sha256("username_2_password".encode()).hexdigest()
username_2_email = "pawel@mmp.co.uk"
username_2_role = "USER"

try:
    cursor.execute("INSERT INTO users (full_name, email, password, role) VALUES (%s, %s, %s, %s)",
                   (username_2_full_name, username_2_email, username_2_password, username_2_role))
    cnx.commit()  # Don't forget to commit the changes.
except mysql.connector.Error as err:
    print(f"Error: {err}")

username_3_full_name = "Maggie A"
username_3_password = hashlib.sha256("username_3_password".encode()).hexdigest()
username_3_email = "maggie@mmp.co.uk"
username_3_role = "USER"

try:
    cursor.execute("INSERT INTO users (full_name, email, password, role) VALUES (%s, %s, %s, %s)",
                   (username_3_full_name, username_3_email, username_3_password, username_3_role))
    cnx.commit()  # Don't forget to commit the changes.
except mysql.connector.Error as err:
    print(f"Error: {err}")

# END IT ALL

cursor.close()
cnx.close()
