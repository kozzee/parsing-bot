import mysql.connector, os


def connection_database(password):
    conn = mysql.connector.connect(
        user='root',
        password=password,
        host='localhost',
        database='rss_search'
    )
    return conn

def insert_user(conn, table, data):
    cursor = conn.cursor(buffered=True)
    
    query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
    cursor.execute(query)

    conn.commit()
    cursor.close()

def check_tgid(conn, tg_id):
    try:
        cursor = conn.cursor()
        sql_query = "SELECT * FROM user WHERE tg_id = %s"
        cursor.execute(sql_query, (tg_id,))
        result = cursor.fetchone()
        cursor.close()   
        return result
    
    except Exception as e:
        return None
    
def add_user(conn, tg_id):
    cursor = conn.cursor(buffered=True)
    query = "INSERT INTO users (tg_id) VALUES (%s)"
    cursor.execute(query, (tg_id,))
    conn.commit()
    cursor.close()
    