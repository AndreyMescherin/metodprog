import os
import logging
import logging.handlers
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LOGGING_DIR = os.path.join(BASE_DIR, 'logs')

# Создаем папку для логов, если её нет
if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)


def setup_logging():
    """
    Настройка логирования для всего проекта
    """
    
    # Общий форматтер для всех хэндлеров
    formatter = logging.Formatter(
        fmt='[%(asctime)s] [%(levelname)-8s] [%(name)-20s] [%(module)s:%(funcName)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Простой форматтер для консоли
    console_formatter = logging.Formatter(
        fmt='[%(asctime)s] %(levelname)-8s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # 1. Консольный хэндлер
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # 2. Файловый хэндлер с ротацией по размеру (10 МБ, 5 файлов)
    file_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(LOGGING_DIR, 'django.log'),
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    # 3. Файловый хэндлер с ротацией по времени (каждый день, хранить 7 дней)
    timed_handler = logging.handlers.TimedRotatingFileHandler(
        filename=os.path.join(LOGGING_DIR, 'daily.log'),
        when='midnight',
        interval=1,
        backupCount=7,
        encoding='utf-8'
    )
    timed_handler.setLevel(logging.INFO)
    timed_handler.setFormatter(formatter)
    
    # 4. Отдельный файл для ошибок
    error_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(LOGGING_DIR, 'errors.log'),
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    
    # 5. Отдельный файл для авторизации
    auth_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(LOGGING_DIR, 'auth.log'),
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding='utf-8'
    )
    auth_handler.setLevel(logging.INFO)
    auth_handler.setFormatter(formatter)
    
    # Настройка корневого логгера
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(timed_handler)
    root_logger.addHandler(error_handler)
    
    # Настройка логгера для авторизации
    auth_logger = logging.getLogger('auth')
    auth_logger.setLevel(logging.INFO)
    auth_logger.addHandler(auth_handler)
    auth_logger.propagate = True  # Также передаёт в корневой логгер
    
    # Настройка логгера для Django
    django_logger = logging.getLogger('django')
    django_logger.setLevel(logging.INFO)
    
    return root_logger