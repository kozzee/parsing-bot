import mysql.connector, os

pas = 'Ibra0550-'
def connection_database(password):
    conn = mysql.connector.connect(
        user='root',
        password=password,
        host='localhost',
        database='rss'
    )
    print(conn)
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
        sql_query = "SELECT * FROM users WHERE tg_id = %s"
        cursor.execute(sql_query, (tg_id,))
        result = cursor.fetchone()
        cursor.close()   
        print(result)
        return result
    
    except Exception as e:
        return None
    
def add_user(conn, tg_id):
    try:
        cursor = conn.cursor(buffered=True)
        query = "INSERT INTO users (tg_id) VALUES (%s)"
        cursor.execute(query, (tg_id,))
        conn.commit()
        cursor.close()
        print(f'Новый пользователь {tg_id}')
    except Exception as e:
        print(f'Ошибка добавления пользователя: {e}')
    