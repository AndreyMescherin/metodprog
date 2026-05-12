import pytest
from django.urls import reverse


class TestPrivacy:
    """Тесты приватности профилей"""
    
    def test_can_see_own_profile(self, logged_client):
        """Пользователь видит свой профиль"""
        response = logged_client.get(reverse('users:profile'))
        assert response.status_code == 200
    
    def test_cannot_see_private_profile(self, logged_client, another_user):
        """Пользователь не видит приватный профиль незнакомца"""
        another_user.is_public = False
        another_user.save()
        
        response = logged_client.get(
            reverse('users:user_detail', args=[another_user.id])
        )
        assert response.status_code == 302
    
    def test_can_see_public_profile(self, logged_client, another_user):
        """Пользователь видит публичный профиль незнакомца"""
        another_user.is_public = True
        another_user.save()
        
        response = logged_client.get(
            reverse('users:user_detail', args=[another_user.id])
        )
        assert response.status_code == 200
    
    def test_friend_can_see_private_profile(self, logged_client, user, another_user):
        """Друг видит приватный профиль"""
        user.add_friend(another_user)
        another_user.is_public = False
        another_user.save()
        
        response = logged_client.get(
            reverse('users:user_detail', args=[another_user.id])
        )
        assert response.status_code == 200
    
    @pytest.mark.parametrize('is_public,is_friend,can_see', [
        (True, True, True),
        (True, False, True),
        (False, True, True),
        (False, False, False),
    ])
    def test_privacy_matrix(self, logged_client, user, another_user, is_public, is_friend, can_see):
        """Параметризованный тест матрицы приватности"""
        another_user.is_public = is_public
        another_user.save()
        
        if is_friend:
            user.add_friend(another_user)
        
        response = logged_client.get(
            reverse('users:user_detail', args=[another_user.id])
        )
        
        if can_see:
            assert response.status_code == 200
        else:
            assert response.status_code == 302
    
    def test_user_list_page(self, logged_client):
        """Страница списка пользователей доступна"""
        response = logged_client.get(reverse('users:user_list'))
        assert response.status_code == 200