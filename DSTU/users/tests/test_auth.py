import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class TestRegistration:
    """Тесты регистрации"""
    
    def test_register_page_accessible(self, client):
        response = client.get(reverse('users:register'))
        assert response.status_code == 200
    
    def test_register_success(self, client, user_data):
        response = client.post(reverse('users:register'), user_data)
        assertRedirects(response, reverse('users:profile'))
        assert User.objects.filter(username='testuser').exists()
    
    def test_register_auto_login(self, client, user_data):
        client.post(reverse('users:register'), user_data)
        response = client.get(reverse('users:profile'))
        assert response.status_code == 200
    
    def test_register_duplicate_email(self, client, user, user_data):
        user_data['username'] = 'newuser'
        response = client.post(reverse('users:register'), user_data)
        assert response.status_code == 200
    
    def test_register_duplicate_username(self, client, user, user_data):
        user_data['email'] = 'new@test.com'
        response = client.post(reverse('users:register'), user_data)
        assert response.status_code == 200
    
    def test_authenticated_cannot_register(self, logged_client):
        response = logged_client.get(reverse('users:register'))
        assertRedirects(response, reverse('schedule:teacher_index'))


class TestLogin:
    """Тесты входа"""
    
    def test_login_page_accessible(self, client):
        response = client.get(reverse('login'))
        assert response.status_code == 200
    
    def test_login_success(self, client, user):
        response = client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'StrongPass123!',
        })
        assertRedirects(response, reverse('schedule:teacher_index'))
    
    @pytest.mark.parametrize('username,password', [
        ('testuser', 'WrongPass!'),
        ('nonexistent', 'AnyPass123!'),
        ('', ''),
    ])
    def test_login_failure(self, client, user, username, password):
        response = client.post(reverse('login'), {
            'username': username,
            'password': password,
        })
        assert response.status_code == 200


class TestLogout:
    """Тесты выхода"""
    
    def test_logout(self, logged_client):
        response = logged_client.post(reverse('logout'))
        assertRedirects(response, reverse('schedule:teacher_index'))
    
    def test_logout_redirect(self, logged_client):
        logged_client.post(reverse('logout'))
        response = logged_client.get(reverse('users:profile'))
        assertRedirects(response, reverse('login') + '?next=' + reverse('users:profile'))


class TestRedirects:
    """Тесты редиректов"""
    
    @pytest.mark.parametrize('url_name,redirect_url', [
        ('users:profile', '/auth/login/'),
        ('users:profile_edit', '/auth/login/'),
        ('users:user_list', '/auth/login/'),
        ('users:friends_list', '/auth/login/'),
    ])
    def test_anonymous_redirects_to_login(self, client, url_name, redirect_url):
        response = client.get(reverse(url_name))
        assert response.status_code == 302
        assert redirect_url in response.url
    
    def test_login_redirects_to_schedule(self, client, user):
        response = client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'StrongPass123!',
        })
        assertRedirects(response, reverse('schedule:teacher_index'))
    
    def test_register_redirects_to_profile(self, client, user_data):
        response = client.post(reverse('users:register'), user_data)
        assertRedirects(response, reverse('users:profile'))


# Импорт для assertRedirects
from django.test import TestCase as _TestCase

def assertRedirects(response, expected_url, status_code=302):
    """Проверка редиректа"""
    assert response.status_code == status_code
    assert response.url == expected_url