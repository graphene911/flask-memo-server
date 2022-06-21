import mysql.connector

def get_connection() :
    connection = mysql.connector.connect(
        host = 'graphene911-db.cett5e9xjv0f.ap-northeast-2.rds.amazonaws.com',
        database = 'memo_api_db',
        user = 'memo_api_user',
        password = 'memo1234'
    )
    return connection
    