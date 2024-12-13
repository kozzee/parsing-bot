import logging, mysql.connector


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') #шаблон для работы логгирования
logger = logging.getLogger(__name__)

def connection_database(password):
    try:
        conn = mysql.connector.connect(
            user='root',
            password=password,
            host='localhost',
            database='rss'
        )
        print("Соединение с базой данных установлено.")
        return conn  # Возвращаем само подключение
    except mysql.connector.Error as e:
        logger.error(f'Ошибка подключения к базе данных: {e}')
        raise  # Передаем исключение дальше
