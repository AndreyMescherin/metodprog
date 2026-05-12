import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


class TestUserModel:
    """Тесты модели пользователя"""
    
    def test_create_user(self, db):
        """Создание обычного пользователя"""
        user = User.objects.create_user(
            username='modeluser',
            email='model@test.com',
            password='ModelPass123!',
            first_name='Иван',
            last_name='Петров',
            phone='+7 (999) 123-45-67',
        )
        assert user.username == 'modeluser'
        assert user.email == 'model@test.com'
        assert user.check_password('ModelPass123!')
        assert user.is_active == True
        assert user.is_superuser == False
        assert user.is_staff == False
    
    def test_create_superuser(self, db):
        """Создание суперпользователя"""
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='AdminPass123!',
        )
        assert superuser.is_superuser == True
        assert superuser.is_staff == True
        assert superuser.is_active == True
    
    def test_user_str_method(self, user):
        """Метод __str__ возвращает полное имя"""
        user_str = str(user)
        assert 'Иван' in user_str or 'Петров' in user_str or user.username in user_str
    
    def test_get_full_name(self, user):
        """Метод get_full_name"""
        full_name = user.get_full_name()
        assert 'Иван' in full_name
        assert 'Петров' in full_name
    
    def test_get_full_name_with_middle(self, db):
        """Полное ФИО с отчеством"""
        user = User.objects.create_user(
            username='fullname',
            email='full@test.com',
            password='TestPass123!',
            first_name='Иван',
            last_name='Петров',
            middle_name='Сергеевич',
        )
        assert user.get_full_name_with_middle() == 'Петров Иван Сергеевич'
    
    def test_get_full_name_without_middle(self, user):
        """ФИО без отчества"""
        full_name = user.get_full_name_with_middle()
        assert 'Сергеевич' not in full_name
    
    @pytest.mark.parametrize('is_public,is_active', [
        (True, True),
        (False, True),
        (True, False),
        (False, False),
    ])
    def test_user_fields(self, db, is_public, is_active):
        """Параметризованный тест полей пользователя"""
        user = User.objects.create_user(
            username=f'user_{is_public}_{is_active}',
            email=f'test_{is_public}@test.com',
            password='TestPass123!',
            is_public=is_public,
            is_active=is_active,
        )
        assert user.is_public == is_public
        assert user.is_active == is_active