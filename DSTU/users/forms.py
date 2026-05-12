from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .utils import resize_image


class CustomUserCreationForm(UserCreationForm):
    """
    Форма регистрации нового пользователя с email и телефоном
    """
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        required=True,
        max_length=20,
        label="Телефон",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7 (999) 123-45-67'
        })
    )
    first_name = forms.CharField(
        required=True,
        label="Имя",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        required=True,
        label="Фамилия",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Минимум 8 символов, не только цифры."
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Введите тот же пароль для подтверждения."
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'first_name', 'last_name', 'password1', 'password2')
        labels = {
            'username': 'Логин',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            import re
            cleaned = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            if not re.match(r'^(\+7|8)\d{10}$', cleaned):
                raise forms.ValidationError('Телефон должен быть в формате: +7 (999) 123-45-67')
        return phone
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('Пользователь с таким email уже существует.')
        return email
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            return first_name.strip().capitalize()
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            return last_name.strip().capitalize()
        return last_name
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data.get('phone', '')
        if commit:
            user.save()
        return user


class ProfileEditForm(forms.ModelForm):
    """Форма редактирования профиля с авто-уменьшением аватара"""
    
    class Meta:
        model = User
        fields = ('email', 'phone', 'first_name', 'last_name', 'middle_name', 
                  'birth_date', 'bio', 'avatar', 'is_public')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
        labels = {
            'is_public': 'Публичный профиль (виден всем)',
            'avatar': 'Фото профиля (любое изображение)',
        }
        help_texts = {
            'avatar': 'Поддерживаются JPG, PNG, GIF, WEBP. Фото будет автоматически уменьшено до 300x300.',
        }
    
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # Проверяем что это изображение
            try:
                from PIL import Image
                img = Image.open(avatar)
                img.verify()  # Проверяем что файл не поврежден
                
                # Проверяем размер файла (макс 10 МБ)
                if avatar.size > 10 * 1024 * 1024:
                    raise forms.ValidationError('Размер файла не должен превышать 10 МБ.')
                
                # Автоматически уменьшаем изображение
                avatar = resize_image(avatar, max_width=300, max_height=300)
                
            except Exception as e:
                raise forms.ValidationError(f'Ошибка загрузки изображения: {e}')
        
        return avatar
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            import re
            cleaned = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            if cleaned and not re.match(r'^(\+7|8)\d{10}$', cleaned):
                raise forms.ValidationError('Телефон должен быть в формате: +7 (999) 123-45-67')
        return phone