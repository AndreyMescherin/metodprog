import pytest
from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def client(db):
    """Фикстура клиента для тестов (с доступом к БД)"""
    return Client()


@pytest.fixture
def user_data():
    """Фикстура с данными пользователя для регистрации"""
    return {
        'username': 'testuser',
        'email': 'test@test.com',
        'phone': '+7 (999) 123-45-67',
        'first_name': 'Иван',
        'last_name': 'Петров',
        'password1': 'StrongPass123!',
        'password2': 'StrongPass123!',
    }


@pytest.fixture
def user(db, user_data):
    """Фикстура созданного пользователя"""
    user = User.objects.create_user(
        username=user_data['username'],
        email=user_data['email'],
        password=user_data['password1'],
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
        phone=user_data.get('phone', ''),
    )
    return user


@pytest.fixture
def another_user(db):
    """Фикстура второго пользователя"""
    user = User.objects.create_user(
        username='anotheruser',
        email='another@test.com',
        password='AnotherPass123!',
        first_name='Петр',
        last_name='Иванов',
        phone='+7 (999) 999-99-99',
    )
    return user


@pytest.fixture
def logged_client(client, user):
    """Фикстура авторизованного клиента"""
    client.login(username='testuser', password='StrongPass123!')
    return client


@pytest.fixture
def superuser(db):
    """Фикстура суперпользователя"""
    return User.objects.create_superuser(
        username='admin',
        email='admin@test.com',
        password='AdminPass123!',
    )