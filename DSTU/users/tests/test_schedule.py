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
        """Параметризованный тест: страницы schedule доступны"""
        response = client.get(reverse(url_name))
        # Большинство страниц доступны всем
        assert response.status_code in [200, 302]
    
    def test_teacher_index_content(self, client):
        """Страница преподавателей содержит правильный заголовок"""
        response = client.get(reverse('schedule:teacher_index'))
        assert response.status_code == 200
        content = response.content.decode()
        assert 'Преподаватели' in content
    
    def test_course_index_content(self, client):
        """Страница курсов содержит правильный заголовок"""
        response = client.get(reverse('schedule:course_index'))
        assert response.status_code == 200
        content = response.content.decode()
        assert 'Курсы' in content
    
    def test_student_index_content(self, client):
        """Страница студентов содержит правильный заголовок"""
        response = client.get(reverse('schedule:student_index'))
        assert response.status_code == 200
        content = response.content.decode()
        assert 'Студенты' in content
    
    def test_orm_queries_accessible(self, client):
        """Страница ORM запросов доступна"""
        response = client.get(reverse('schedule:orm_queries'))
        assert response.status_code == 200


class TestErrors:
    """Тесты обработки ошибок"""
    
    def test_nonexistent_user_404(self, logged_client):
        """404 при запросе несуществующего пользователя"""
        response = logged_client.get(
            reverse('users:user_detail', args=[99999])
        )
        assert response.status_code == 404
    
    def test_profile_edit_invalid(self, logged_client):
        """Невалидный POST при редактировании профиля"""
        response = logged_client.post(reverse('users:profile_edit'), {
            'email': 'invalid-email',
            'first_name': '',
            'last_name': '',
        })
        assert response.status_code == 200
    
    def test_profile_edit_valid(self, logged_client):
        """Валидный POST при редактировании профиля"""
        response = logged_client.post(reverse('users:profile_edit'), {
            'email': 'valid@test.com',
            'first_name': 'Тест',
            'last_name': 'Тестов',
            'phone': '+7 (999) 123-45-67',
        })
        assert response.status_code == 302