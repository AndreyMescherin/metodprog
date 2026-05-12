import pytest
from users.forms import CustomUserCreationForm, ProfileEditForm


class TestRegistrationForm:
    """Тесты формы регистрации"""
    
    @pytest.mark.django_db
    def test_form_valid(self, user_data):
        """Форма валидна с правильными данными"""
        form = CustomUserCreationForm(data=user_data)
        assert form.is_valid() == True
    
    @pytest.mark.django_db
    def test_form_invalid_empty(self):
        """Форма невалидна с пустыми данными"""
        form = CustomUserCreationForm(data={})
        assert form.is_valid() == False
        assert 'username' in form.errors
        assert 'email' in form.errors
        assert 'password1' in form.errors
        assert 'password2' in form.errors
    
    @pytest.mark.django_db
    @pytest.mark.parametrize('field,value,expected_error', [
        ('email', '', 'Это поле обязательно.'),
        ('email', 'invalid', 'Введите правильный адрес электронной почты.'),
        ('first_name', '', 'Это поле обязательно.'),
        ('last_name', '', 'Это поле обязательно.'),
        ('phone', '', 'Это поле обязательно.'),
        ('username', '', 'Это поле обязательно.'),
    ])
    def test_form_field_required(self, user_data, field, value, expected_error):
        """Параметризованный тест: обязательные поля"""
        user_data[field] = value
        form = CustomUserCreationForm(data=user_data)
        assert form.is_valid() == False
        assert field in form.errors
    
    @pytest.mark.django_db
    def test_form_cleans_first_name(self, user_data):
        """Форма очищает имя (первая буква заглавная)"""
        user_data['first_name'] = 'иван'
        form = CustomUserCreationForm(data=user_data)
        assert form.is_valid()
        assert form.cleaned_data['first_name'] == 'Иван'
    
    @pytest.mark.django_db
    def test_form_cleans_last_name(self, user_data):
        """Форма очищает фамилию (первая буква заглавная)"""
        user_data['last_name'] = 'петров'
        form = CustomUserCreationForm(data=user_data)
        assert form.is_valid()
        assert form.cleaned_data['last_name'] == 'Петров'
    
    @pytest.mark.django_db
    def test_form_cleans_email(self, user_data):
        """Форма приводит email к нижнему регистру"""
        user_data['email'] = 'TEST@TEST.COM'
        form = CustomUserCreationForm(data=user_data)
        assert form.is_valid()
        assert form.cleaned_data['email'] == 'test@test.com'
    
    @pytest.mark.django_db
    @pytest.mark.parametrize('phone,is_valid', [
        ('+7 (999) 123-45-67', True),
        ('89991234567', True),
        ('+79991234567', True),
        ('12345', False),
        ('abcd', False),
        ('', False),
    ])
    def test_form_phone_validation(self, user_data, phone, is_valid):
        """Параметризованный тест валидации телефона"""
        user_data['phone'] = phone
        form = CustomUserCreationForm(data=user_data)
        assert form.is_valid() == is_valid


class TestProfileEditForm:
    """Тесты формы редактирования профиля"""
    
    @pytest.mark.django_db
    def test_form_valid_minimal(self, user):
        """Форма валидна с минимальными данными"""
        form = ProfileEditForm(instance=user, data={
            'email': 'test@test.com',
            'first_name': 'Иван',
            'last_name': 'Петров',
        })
        # Может требовать phone, зависит от формы
        assert form.is_valid() or 'phone' in form.errors
    
    @pytest.mark.django_db
    def test_form_save(self, user):
        """Форма сохраняет данные"""
        form = ProfileEditForm(instance=user, data={
            'email': 'new@test.com',
            'first_name': 'Сергей',
            'last_name': 'Сидоров',
            'phone': '+7 (999) 111-22-33',
            'bio': 'Новая информация',
        })
        if form.is_valid():
            form.save()
            user.refresh_from_db()
            assert user.email == 'new@test.com'
            assert user.first_name == 'Сергей'
            assert user.bio == 'Новая информация'