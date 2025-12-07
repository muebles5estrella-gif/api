import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="manueldev.55",
        database="sign_technology",
        cursorclass=pymysql.cursors.DictCursor
    )
