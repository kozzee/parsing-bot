import mysql.connector, os
from config import logger

def connection_database(password):
    conn = mysql.connector.connect(
        user='root',
        password=password,
        host='localhost',
        database='rss'
    )
    print(conn)
    return conn


# def insert_user(conn, table, data):
#     cursor = conn.cursor(buffered=True)
    
#     query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
#     cursor.execute(query)

#     conn.commit()
#     cursor.close()

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
        print(f'Новый пользователь {tg_id}')
        return True
    except mysql.connector.Error as e:
        print(f'Ошибка добавления пользователя в базу: {e}')
        logger.error(f'Ошибка добавления пользователя в базу: {e}')
        return False
    finally:
        if cursor:
            cursor.close()


def get_from_database(conn, data, table, value=''):
    try:
        cursor = conn.cursor()
        if value:
            query = f"SELECT {data} FROM {table} WHERE {value}"
        else:
            query = f"SELECT {data} FROM {table}"
        cursor.execute(query)
        result = [row[0] for row in cursor.fetchall()]
        return result
    except mysql.connector.Error as e:
        print(f'Ошибка получения данных из базы: {e}')
        logger.error(f'Ошибка получения данных из базы: {e}')
        return None
    finally:
        if cursor:
            cursor.close()


    


    