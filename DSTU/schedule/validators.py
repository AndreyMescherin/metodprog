from django.core.exceptions import ValidationError
from datetime import date
import re


# КАСТОМНЫЕ ВАЛИДАТОРЫ

def validate_phone_format(value):
    """
    Валидатор 1: Проверка формата телефона
    Должен быть в формате: +7XXXXXXXXXX или 8XXXXXXXXXX
    """
    # Убираем все лишние символы
    cleaned = value.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    
    # Паттерн для российского номера
    pattern = r'^(\+7|8)\d{10}$'
    
    if not re.match(pattern, cleaned):
        raise ValidationError(
            'Телефон должен быть в формате: +7 (999) 123-45-67 или 89991234567'
        )


def validate_future_date(value):
    """
    Валидатор 2: Проверка, что дата не в прошлом
    Используется для даты начала курса
    """
    if value < date.today():
        raise ValidationError(
            'Дата не может быть в прошлом. Выберите будущую дату.'
        )


def validate_adult_age(value):
    """
    Валидатор 3: Проверка совершеннолетия (18+)
    Используется для даты рождения
    """
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    
    if age < 18:
        raise ValidationError(
            'Возраст должен быть не менее 18 лет.'
        )
    if age > 100:
        raise ValidationError(
            'Проверьте правильность даты рождения. Возраст не может быть больше 100 лет.'
        )


def format_phone(value):
    """
    Форматирование телефона в единый стиль: +7 (XXX) XXX-XX-XX
    """
    # Убираем все лишние символы
    cleaned = value.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    
    # Если начинается с 8, заменяем на +7
    if cleaned.startswith('8'):
        cleaned = '+7' + cleaned[1:]
    elif not cleaned.startswith('+7'):
        if len(cleaned) == 10:
            cleaned = '+7' + cleaned
    
    # Форматируем если номер корректной длины
    if len(cleaned) == 12:  # +7 + 10 цифр
        formatted = f"{cleaned[:2]} ({cleaned[2:5]}) {cleaned[5:8]}-{cleaned[8:10]}-{cleaned[10:12]}"
        return formatted
    return value


def format_passport(value):
    """
    Форматирование паспорта в формат: XXXX XXXXXX
    """
    # Убираем все пробелы
    cleaned = value.replace(' ', '')
    
    # Форматируем
    if len(cleaned) == 10:
        formatted = f"{cleaned[:4]} {cleaned[4:]}"
        return formatted
    return value


def format_name(value):
    """
    Форматирование имени/фамилии: первая буква заглавная, остальные строчные
    """
    if value:
        # Разбиваем на слова (для двойных фамилий)
        words = value.split()
        formatted_words = [word.capitalize() for word in words]
        return ' '.join(formatted_words)
    return value