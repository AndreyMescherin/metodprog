from django import forms
from .models import Teacher, TeacherInfo, Course, Student

# НОВАЯ ФОРМА ДЛЯ ЛАБОРАТОРНОЙ РАБОТЫ
class TeacherForm(forms.Form):
    """Форма для добавления преподавателя с использованием forms.Form"""
    first_name = forms.CharField(
        max_length=50,
        label='Имя',
        help_text='Введите имя преподавателя',
        widget=forms.TextInput(attrs={
            'placeholder': 'Например: Иван',
            'class': 'form-control'
        })
    )
    last_name = forms.CharField(
        max_length=50,
        label='Фамилия',
        help_text='Введите фамилию преподавателя',
        widget=forms.TextInput(attrs={
            'placeholder': 'Например: Петров',
            'class': 'form-control'
        })
    )
    email = forms.EmailField(
        label='Email',
        help_text='Введите email для связи',
        widget=forms.EmailInput(attrs={
            'placeholder': 'ivan.petrov@example.com',
            'class': 'form-control'
        })
    )
    phone = forms.CharField(
        max_length=20,
        label='Телефон',
        required=False,  # Необязательное поле
        help_text='Введите номер телефона (необязательно)',
        widget=forms.TextInput(attrs={
            'placeholder': '+7 (999) 123-45-67',
            'class': 'form-control'
        })
    )
    hire_date = forms.DateField(
        label='Дата найма',
        help_text='Выберите дату начала работы',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    salary = forms.DecimalField(
        label='Зарплата',
        required=False,
        help_text='Укажите зарплату (необязательно)',
        widget=forms.NumberInput(attrs={
            'placeholder': '50000.00',
            'step': '0.01',
            'class': 'form-control'
        })
    )

class TeacherInfoForm(forms.ModelForm):
    class Meta:
        model = TeacherInfo
        fields = ['address', 'birth_date', 'education', 'experience_years', 'bio', 'office_number']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'credits', 'level', 'duration_weeks', 'price', 'teacher']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'phone', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'phone': 'Телефон',
            'birth_date': 'Дата рождения',
        }