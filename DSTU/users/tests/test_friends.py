import pytest
from django.urls import reverse


class TestFriends:
    """Тесты системы друзей"""
    
    def test_add_friend(self, logged_client, user, another_user):
        """Добавление в друзья"""
        response = logged_client.get(
            reverse('users:add_friend', args=[another_user.id])
        )
        assert response.status_code == 302
        user.refresh_from_db()
        assert user.is_friend(another_user) == True
    
    def test_remove_friend(self, logged_client, user, another_user):
        """Удаление из друзей"""
        user.add_friend(another_user)
        assert user.is_friend(another_user) == True
        
        response = logged_client.get(
            reverse('users:remove_friend', args=[another_user.id])
        )
        assert response.status_code == 302
        user.refresh_from_db()
        assert user.is_friend(another_user) == False
    
    def test_cannot_add_self(self, logged_client, user):
        """Нельзя добавить себя в друзья"""
        response = logged_client.get(
            reverse('users:add_friend', args=[user.id])
        )
        assert response.status_code == 302
        user.refresh_from_db()
        assert user.is_friend(user) == False
    
    def test_add_friend_twice(self, logged_client, user, another_user):
        """Двойное добавление не вызывает ошибки"""
        user.add_friend(another_user)
        response = logged_client.get(
            reverse('users:add_friend', args=[another_user.id])
        )
        assert response.status_code == 302
        assert user.is_friend(another_user) == True
    
    def test_friends_list_page(self, logged_client):
        """Страница списка друзей доступна"""
        response = logged_client.get(reverse('users:friends_list'))
        assert response.status_code == 200
    
    def test_friends_count_zero(self, user):
        """Новый пользователь имеет 0 друзей"""
        assert user.get_friends_count() == 0
    
    def test_friends_count_after_adding(self, user, another_user):
        """Количество друзей после добавления"""
        user.add_friend(another_user)
        assert user.get_friends_count() == 1
    
    @pytest.mark.parametrize('action,expected_friend', [
        ('add_friend', True),
        ('remove_friend', False),
    ])
    def test_friend_actions(self, logged_client, user, another_user, action, expected_friend):
        """Параметризованный тест действий с друзьями"""
        if action == 'add_friend':
            if not user.is_friend(another_user):
                user.add_friend(another_user)
            response = logged_client.get(
                reverse('users:add_friend', args=[another_user.id])
            )
        else:
            if not user.is_friend(another_user):
                user.add_friend(another_user)
            response = logged_client.get(
                reverse('users:remove_friend', args=[another_user.id])
            )
        
        assert response.status_code == 302
        user.refresh_from_db()
        assert user.is_friend(another_user) == expected_friend