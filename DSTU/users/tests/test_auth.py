import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class TestRegistration:
    """Тесты регистрации"""
    
    def test_register_page_accessible(self, client):
        """Страница регистрации доступна"""
        response = client.get(reverse('users:register'))
        assert response.status_code == 200
    
    def test_register_success(self, client, user_data):
        """Успешная регистрация"""
        response = client.post(reverse('users:register'), user_data)
        assert response.status_code == 302
        assert response.url == reverse('users:profile')
        assert User.objects.filter(username='testuser').exists()
    
    def test_register_auto_login(self, client, user_data):
        """Автоматический вход после регистрации"""
        client.post(reverse('users:register'), user_data)
        response = client.get(reverse('users:profile'))
        assert response.status_code == 200
    
    def test_register_duplicate_email(self, client, user, user_data):
        """Регистрация с существующим email"""
        user_data['username'] = 'newuser'
        response = client.post(reverse('users:register'), user_data)
        assert response.status_code == 200
    
    def test_register_duplicate_username(self, client, user, user_data):
        """Регистрация с существующим username"""
        user_data['email'] = 'new@test.com'
        response = client.post(reverse('users:register'), user_data)
        assert response.status_code == 200
    
    def test_authenticated_cannot_register(self, logged_client):
        """Авторизованный не может зарегистрироваться"""
        response = logged_client.get(reverse('users:register'))
        assert response.status_code == 302


class TestLogin:
    """Тесты входа"""
    
    def test_login_page_accessible(self, client):
        """Страница входа доступна"""
        response = client.get(reverse('login'))
        assert response.status_code == 200
    
    def test_login_success(self, client, user):
        """Успешный вход"""
        response = client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'StrongPass123!',
        })
        assert response.status_code == 302
        assert response.url == reverse('schedule:teacher_index')
    
    @pytest.mark.parametrize('username,password', [
        ('testuser', 'WrongPass!'),
        ('nonexistent', 'AnyPass123!'),
        ('', ''),
    ])
    def test_login_failure(self, client, user, username, password):
        """Параметризованный тест: неудачный вход"""
        response = client.post(reverse('login'), {
            'username': username,
            'password': password,
        })
        assert response.status_code == 200


class TestLogout:
    """Тесты выхода"""
    
    def test_logout(self, logged_client):
        """Успешный выход"""
        response = logged_client.post(reverse('logout'))
        assert response.status_code == 302
        assert response.url == reverse('schedule:teacher_index')
    
    def test_logout_redirect(self, logged_client):
        """После выхода редирект"""
        logged_client.post(reverse('logout'))
        response = logged_client.get(reverse('users:profile'))
        assert response.status_code == 302


class TestRedirects:
    """Тесты редиректов"""
    
    @pytest.mark.parametrize('url_name', [
        'users:profile',
        'users:profile_edit',
        'users:user_list',
        'users:friends_list',
    ])
    def test_anonymous_redirects_to_login(self, client, url_name):
        """Аноним редиректится на логин"""
        response = client.get(reverse(url_name))
        assert response.status_code == 302
        assert '/auth/login/' in response.url
    
    def test_login_redirects_to_schedule(self, client, user):
        """После входа редирект на расписание"""
        response = client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'StrongPass123!',
        })
        assert response.status_code == 302
        assert response.url == reverse('schedule:teacher_index')
    
    def test_register_redirects_to_profile(self, client, user_data):
        """После регистрации редирект на профиль"""
        response = client.post(reverse('users:register'), user_data)
        assert response.status_code == 302
        assert response.url == reverse('users:profile')