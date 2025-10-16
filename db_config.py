import pymysql

DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = ""
DB_NAME = "shs_registration"
DB_PORT = 3306

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        port=DB_PORT
    )
