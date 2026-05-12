import pytest
from django.urls import reverse


class TestFriends:
    """Тесты системы друзей"""
    
    def test_add_friend(self, logged_client, user, another_user):
        response = logged_client.get(
            reverse('users:add_friend', args=[another_user.id])
        )
        assertRedirects(response, reverse('users:user_detail', args=[another_user.id]))
        user.refresh_from_db()
        assert user.is_friend(another_user) == True
    
    def test_remove_friend(self, logged_client, user, another_user):
        user.add_friend(another_user)
        assert user.is_friend(another_user) == True
        
        response = logged_client.get(
            reverse('users:remove_friend', args=[another_user.id])
        )
        assertRedirects(response, reverse('users:user_detail', args=[another_user.id]))
        user.refresh_from_db()
        assert user.is_friend(another_user) == False
    
    def test_cannot_add_self(self, logged_client, user):
        response = logged_client.get(
            reverse('users:add_friend', args=[user.id])
        )
        assertRedirects(response, reverse('users:user_detail', args=[user.id]))
        user.refresh_from_db()
        assert user.is_friend(user) == False
    
    def test_add_friend_twice(self, logged_client, user, another_user):
        user.add_friend(another_user)
        response = logged_client.get(
            reverse('users:add_friend', args=[another_user.id])
        )
        assertRedirects(response, reverse('users:user_detail', args=[another_user.id]))
        assert user.is_friend(another_user) == True
    
    def test_friends_list_page(self, logged_client):
        response = logged_client.get(reverse('users:friends_list'))
        assert response.status_code == 200
    
    def test_friends_count_zero(self, user):
        assert user.get_friends_count() == 0
    
    def test_friends_count_after_adding(self, user, another_user):
        user.add_friend(another_user)
        assert user.get_friends_count() == 1
    
    @pytest.mark.parametrize('action,expected_friend', [
        ('add_friend', True),
        ('remove_friend', False),
    ])
    def test_friend_actions(self, logged_client, user, another_user, action, expected_friend):
        if action == 'remove_friend':
            user.add_friend(another_user)
        
        response = logged_client.get(
            reverse(f'users:{action}', args=[another_user.id])
        )
        assertRedirects(response, reverse('users:user_detail', args=[another_user.id]))
        user.refresh_from_db()
        assert user.is_friend(another_user) == expected_friend


def assertRedirects(response, expected_url, status_code=302):
    """Проверка редиректа"""
    assert response.status_code == status_code, f"Expected {status_code}, got {response.status_code}"
    assert response.url == expected_url, f"Expected redirect to {expected_url}, got {response.url}"