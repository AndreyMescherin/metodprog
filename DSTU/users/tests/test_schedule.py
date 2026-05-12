import pytest
from django.urls import reverse


class TestScheduleAccess:
    """Тесты доступа к приложению schedule"""
    
    @pytest.mark.parametrize('url_name', [
        'schedule:teacher_index',
        'schedule:teacher_create',
        'schedule:course_index',
        'schedule:course_create',
        'schedule:student_index',
        'schedule:student_create',
        'schedule:orm_queries',
    ])
    def test_schedule_pages_accessible(self, client, url_name):
        response = client.get(reverse(url_name))
        assert response.status_code in [200, 302]
    
    def test_teacher_index_content(self, client):
        response = client.get(reverse('schedule:teacher_index'))
        assert response.status_code == 200
        assert 'Преподаватели' in response.content.decode()
    
    def test_course_index_content(self, client):
        response = client.get(reverse('schedule:course_index'))
        assert response.status_code == 200
        assert 'Курсы' in response.content.decode()
    
    def test_student_index_content(self, client):
        response = client.get(reverse('schedule:student_index'))
        assert response.status_code == 200
        assert 'Студенты' in response.content.decode()
    
    def test_orm_queries_accessible(self, client):
        response = client.get(reverse('schedule:orm_queries'))
        assert response.status_code == 200


class TestErrors:
    """Тесты обработки ошибок"""
    
    def test_nonexistent_user_404(self, logged_client):
        response = logged_client.get(
            reverse('users:user_detail', args=[99999])
        )
        assert response.status_code == 404
    
    def test_profile_edit_invalid(self, logged_client):
        response = logged_client.post(reverse('users:profile_edit'), {
            'email': 'invalid-email',
            'first_name': '',
            'last_name': '',
        })
        assert response.status_code == 200
    
    def test_profile_edit_valid(self, logged_client):
        response = logged_client.post(reverse('users:profile_edit'), {
            'email': 'valid@test.com',
            'first_name': 'Тест',
            'last_name': 'Тестов',
            'phone': '+7 (999) 123-45-67',
        })
        assertRedirects(response, reverse('users:profile'))


def assertRedirects(response, expected_url, status_code=302):
    """Проверка редиректа"""
    assert response.status_code == status_code, f"Expected {status_code}, got {response.status_code}"
    assert response.url == expected_url, f"Expected redirect to {expected_url}, got {response.url}"