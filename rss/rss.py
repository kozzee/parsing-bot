import mysql.connector, os
from config import logger
import requests
from bs4 import BeautifulSoup

import mysql.connector

def connection_database(password):
    try:
        with mysql.connector.connect(
            user='root',
            password=password,
            host='localhost',
            database='rss'
        ) as conn:
            print("Соединение с базой данных установлено.")
            yield conn  # Возвращаем соединение как генератор для использования в with
    except mysql.connector.Error as e:
        logger.error(f'Ошибка подключения к базе данных: {e}')
        raise  # Передаем исключение дальше



def check_tgid(conn, tg_id):
    try:
        cursor = conn.cursor()
        sql_query = "SELECT * FROM users WHERE tg_id = %s"
        cursor.execute(sql_query, (tg_id,))
        result = cursor.fetchone()
        cursor.close()   
        print(result)
        return result
    
    except mysql.connector.Error as e:
        print(f'Ошибка проверки пользователя в базе: {e}')
        logger.error(f'Ошибка проверки пользователя в базе: {e}')
        #если пользователь не найден, возвращаем None
        return None
    
def add_user(conn, tg_id):
    #Добавляем пользователя в базу данных
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


def get_from_database(conn, data, table, condition=None, params=None):     #получаем данные из базы данных
    """
    Получает данные из базы данных.

    Args:
        conn: Объект подключения к базе данных.
        data: Список названий столбцов.
        table: Название таблицы.
        condition: Условие для выборки данных (необязательный параметр).
        params: Список параметров для условия (необязательный параметр).

    Returns:
        Список кортежей с данными, если данные получены успешно, иначе None.
    """
    try:
        cursor = conn.cursor() 
        columns = ', '.join(data) #соединяем названия столбцов в строку

        if condition:   
            query = f"SELECT {columns} FROM {table} WHERE {condition}" # формируем запрос в базу
        else:
            query = f"SELECT {columns} FROM {table}"

        cursor.execute(query, params)

        result = cursor.fetchall() 
        return result
    except mysql.connector.Error as e:
        print(f'Ошибка получения данных из базы: {e}')
        logger.error(f'Ошибка получения данных из базы: {e}')
        return None
    finally:
        if cursor:
            cursor.close()

def add_data(conn, table, columns, values):
    """
    Добавляет данные в таблицу базы данных.

    Args:
        conn: Объект подключения к базе данных.
        table: Название таблицы.
        columns: Список названий столбцов.
        values: Список значений для добавления.

    Returns:
        True, если данные успешно добавлены, иначе False.
    """
    try:
        cursor = conn.cursor()
        placeholders = ', '.join(['%s'] * len(columns))  # Создаем плейсхолдеры для значений
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        cursor.execute(query, values)
        conn.commit()        
        return True
    except mysql.connector.Error as e:
        print(f'Ошибка добавления данных в базу: {e}')
        logger.error(f'ошибка добавления данных в базу: {e}')
        return False
    finally:
        if cursor:
            cursor.close()

    

def check_data(conn, table, first_value_column, second_value_column, first_value, second_value):
    """
    Проверяет наличие данных в таблице, удовлетворяющих заданным условиям.

    Args:
        conn: Объект подключения к базе данных.
        table: Название таблицы.
        first_value_column: Название столбца для первого условия.
        second_value_column: Название столбца для второго условия.
        first_value: Значение для сравнения в первом условии.
        second_value: Значение для сравнения во втором условии.

    Returns:
        Список кортежей с результатами запроса или None, если произошла ошибка.
    """
    try:
        cursor = conn.cursor()
        query = f"SELECT 1 FROM {table} WHERE {first_value_column} = %s AND {second_value_column} = %s"
        cursor.execute(query, (first_value, second_value))
        result = cursor.fetchone()
        return bool(result)
    except mysql.connector.Error as e:
        print(f'Ошибка проверки данных: {e}')
        logger.error(f'Ошибка проверки данных: {e}')
    finally:
        if cursor:
            cursor.close()



def get_subscription_id_from_database(conn, user_id):
    try:
        cursor = conn.cursor()
        query = f"SELECT source_id FROM subscriptions WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        return [row[0] for row in result] if result else []  # Возвращаем список source_id или пустой список, если подписок нет
    except mysql.connector.Error as e:
        print(f'Ошибка получения ID подписки из базы данных: {e}')
        logger.error(f'Ошибка получения ID подписки из базы данных: {e}')
        return None
    finally:
        if cursor:
            cursor.close()






from bs4 import BeautifulSoup
import requests

def parsing_url(list_url):
    results = []
    for url in list_url:    
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml-xml')
            channel = soup.find('channel')
            if channel:
                item = channel.find('item')
                if item:
                    title = item.find('title')
                    description = item.find('description')
                    link = item.find('link') #Ищем ссылку

                    title_text = title.text if title else "Заголовок отсутствует"
                    description_text = description.text if description else "Описание отсутствует"
                    link_text = link.text if link else "Ссылка отсутствует" 

                    results.append((title_text, description_text, link_text)) # Ссылку в результат
                else:
                    logger.error(f"Ошибка парсинга URL {url}: Тег <item> не найден")
            else:
                 logger.error(f"Ошибка парсинга URL {url}: Тег <channel> не найден")
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе к URL {url}: {e}")
        except (AttributeError, IndexError) as e: 
            logger.error(f"Ошибка парсинга URL {url}: {e}")
    return results






