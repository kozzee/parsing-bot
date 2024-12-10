import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') #шаблон для работы логгирования
logger = logging.getLogger(__name__)