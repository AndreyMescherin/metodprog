import pytest
from django.urls import reverse


class TestPrivacy:
    """Тесты приватности профилей"""
    
    def test_can_see_own_profile(self, logged_client):
        response = logged_client.get(reverse('users:profile'))
        assert response.status_code == 200
    
    def test_cannot_see_private_profile(self, logged_client, another_user):
        another_user.is_public = False
        another_user.save()
        
        response = logged_client.get(
            reverse('users:user_detail', args=[another_user.id])
        )
        assertRedirects(response, reverse('users:user_list'))
    
    def test_can_see_public_profile(self, logged_client, another_user):
        another_user.is_public = True
        another_user.save()
        
        response = logged_client.get(
            reverse('users:user_detail', args=[another_user.id])
        )
        assert response.status_code == 200
    
    def test_friend_can_see_private_profile(self, logged_client, user, another_user):
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
            assertRedirects(response, reverse('users:user_list'))
    
    def test_user_list_page(self, logged_client):
        response = logged_client.get(reverse('users:user_list'))
        assert response.status_code == 200


def assertRedirects(response, expected_url, status_code=302):
    """Проверка редиректа"""
    assert response.status_code == status_code, f"Expected {status_code}, got {response.status_code}"
    assert response.url == expected_url, f"Expected redirect to {expected_url}, got {response.url}"