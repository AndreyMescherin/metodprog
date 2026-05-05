from django import forms
from django.core.exceptions import ValidationError
from .models import Teacher, TeacherInfo, Course, Student
from .validators import (
    validate_phone_format, 
    validate_future_date, 
    validate_adult_age,
    format_phone,
    format_passport,
    format_name
)
from datetime import date


class TeacherForm(forms.ModelForm):
    """
    Форма для Teacher на основе ModelForm
    """
    class Meta:
        model = Teacher
        fields = [
            'first_name', 'last_name', 'email', 'phone', 
            'hire_date', 'salary', 'department', 'academic_degree',
            'office_hours', 'is_active', 'rating'
        ]
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'office_hours': forms.TextInput(attrs={'placeholder': 'Пн-Пт 10:00-12:00'}),
            'rating': forms.NumberInput(attrs={'step': '0.1', 'min': '0', 'max': '5'}),
        }
    
    # Метод clean_first_name - форматирует имя
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            # Форматируем: первая буква заглавная, остальные строчные
            return format_name(first_name)
        return first_name
    
    # Метод clean_last_name - форматирует фамилию
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            # Форматируем: первая буква заглавная, остальные строчные
            return format_name(last_name)
        return last_name
    
    # Метод clean_phone - валидирует и форматирует телефон
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Сначала валидируем
            validate_phone_format(phone)
            # Затем форматируем в красивый вид
            return format_phone(phone)
        return phone
    
    # Метод clean_email - приводит к нижнему регистру
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Приводим к нижнему регистру
            email = email.lower().strip()
            
            # Проверка на допустимые домены
            allowed_domains = ['gmail.com', 'yandex.ru', 'mail.ru', 'edu.ru']
            domain = email.split('@')[1] if '@' in email else ''
            
            if domain and domain not in allowed_domains:
                raise ValidationError(
                    f'Email должен быть из следующих доменов: {", ".join(allowed_domains)}'
                )
            return email
        return email
    
    # Метод clean_salary - округляет до 2 знаков
    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary:
            # Округляем до 2 знаков после запятой
            salary = round(salary, 2)
            
            if salary > 500000:
                raise ValidationError(
                    'Зарплата не может превышать 500 000 рублей. Проверьте правильность ввода.'
                )
            return salary
        return salary
    
    # Метод clean_department - форматирует название кафедры
    def clean_department(self):
        department = self.cleaned_data.get('department')
        if department:
            # Убираем лишние пробелы в начале и конце
            department = department.strip()
            # Каждое слово с заглавной буквы
            words = department.split()
            department = ' '.join([word.capitalize() for word in words])
            return department
        return department
    
    # Общий clean() для формы
    def clean(self):
        cleaned_data = super().clean()
        
        # Автоматически устанавливаем rating = 0, если не указан
        if not cleaned_data.get('rating'):
            cleaned_data['rating'] = 0
        
        # Если преподаватель не активен, рейтинг должен быть 0
        if cleaned_data.get('is_active') == False:
            cleaned_data['rating'] = 0
        
        # Проверка: имя и фамилия не должны совпадать
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        if first_name and last_name and first_name.lower() == last_name.lower():
            raise ValidationError(
                'Имя и фамилия не должны совпадать.'
            )
        
        # Проверка: дата найма не может быть в будущем
        # Если дата из будущего, устанавливаем сегодняшнюю дату
        hire_date = cleaned_data.get('hire_date')
        if hire_date and hire_date > date.today():
            cleaned_data['hire_date'] = date.today()
            # Добавляем предупреждение через форму
            self.add_warning('Дата найма была автоматически изменена на сегодняшнюю.')
        
        return cleaned_data
    
    def add_warning(self, message):
        """Добавляет предупреждение в форму"""
        if not hasattr(self, '_warnings'):
            self._warnings = []
        self._warnings.append(message)


class TeacherInfoForm(forms.ModelForm):
    class Meta:
        model = TeacherInfo
        fields = [
            'address', 'birth_date', 'education', 'experience_years', 
            'bio', 'office_number', 'passport_number', 'marital_status',
            'publications_count', 'emergency_contact'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
    
    # Метод clean_education - форматирует строку
    def clean_education(self):
        education = self.cleaned_data.get('education')
        if education:
            # Убираем лишние пробелы
            education = education.strip()
            # Первая буква заглавная
            education = education[0].upper() + education[1:] if education else education
            return education
        return education
    
    # Метод clean_experience_years - автоматически округляет
    def clean_experience_years(self):
        experience = self.cleaned_data.get('experience_years')
        if experience is not None:
            # Если больше 50, автоматически уменьшаем до 50
            if experience > 50:
                experience = 50
            if experience < 0:
                experience = 0
            return experience
        return experience
    
    # Метод clean_passport_number - форматирует номер паспорта
    def clean_passport_number(self):
        passport = self.cleaned_data.get('passport_number')
        if passport:
            # Убираем лишние пробелы и форматируем
            passport = passport.strip()
            passport = format_passport(passport)
            return passport
        return passport
    
    # Метод clean_emergency_contact - форматирует телефон
    def clean_emergency_contact(self):
        phone = self.cleaned_data.get('emergency_contact')
        if phone:
            # Валидируем и форматируем как телефон
            validate_phone_format(phone)
            return format_phone(phone)
        return phone
    
    # Метод clean_address - приводит к стандартному виду
    def clean_address(self):
        address = self.cleaned_data.get('address')
        if address:
            # Убираем множественные пробелы
            address = ' '.join(address.split())
            # Первая буква заглавная
            address = address.capitalize()
            return address
        return address
    
    # Метод clean_birth_date - проверяет совершеннолетие
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            validate_adult_age(birth_date)
        return birth_date
    
    # Общий clean() для формы
    def clean(self):
        cleaned_data = super().clean()
        
        # Автоматически устанавливаем количество публикаций в 0, если не указано
        if cleaned_data.get('publications_count') is None:
            cleaned_data['publications_count'] = 0
        
        # Если опыт работы не указан, ставим 0
        if cleaned_data.get('experience_years') is None:
            cleaned_data['experience_years'] = 0
        
        # Автоматически формируем bio, если оно пустое
        if not cleaned_data.get('bio') and cleaned_data.get('education'):
            education = cleaned_data.get('education')
            experience = cleaned_data.get('experience_years', 0)
            cleaned_data['bio'] = f"Образование: {education}. Опыт работы: {experience} лет."
        
        return cleaned_data


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title', 'description', 'credits', 'level', 
            'duration_weeks', 'price', 'teacher', 'max_students',
            'syllabus', 'prerequisites', 'is_online', 'start_date'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'syllabus': forms.Textarea(attrs={'rows': 3}),
            'prerequisites': forms.Textarea(attrs={'rows': 3}),
        }
    
    # Метод clean_title - форматирует название курса
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title:
            # Убираем лишние пробелы
            title = title.strip()
            # Каждое слово с заглавной буквы
            words = title.split()
            title = ' '.join([word.capitalize() for word in words])
            return title
        return title
    
    # Метод clean_start_date - проверяет будущую дату
    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date:
            validate_future_date(start_date)
        return start_date
    
    # Метод clean_price - форматирует цену
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price:
            # Округляем до 2 знаков
            price = round(price, 2)
            
            # Если цена больше 1 000 000, уменьшаем до максимума
            if price > 1000000:
                price = 1000000
            
            # Автоматически делаем цену кратной 100 при стоимости > 10000
            if price > 10000:
                price = round(price / 100) * 100
            
            return price
        return price
    
    # Метод clean_credits - автоматически корректирует
    def clean_credits(self):
        credits = self.cleaned_data.get('credits')
        if credits:
            if credits > 10:
                credits = 10
            if credits < 1:
                credits = 1
            return credits
        return credits
    
    # Метод clean_duration_weeks - автоматически корректирует
    def clean_duration_weeks(self):
        duration = self.cleaned_data.get('duration_weeks')
        if duration:
            if duration < 1:
                duration = 1
            if duration > 52:  # максимум год
                duration = 52
            return duration
        return duration
    
    # Общий clean() для формы
    def clean(self):
        cleaned_data = super().clean()
        
        # Автоматически устанавливаем max_students в зависимости от типа курса
        is_online = cleaned_data.get('is_online')
        max_students = cleaned_data.get('max_students')
        
        if is_online and max_students:
            # Для онлайн курсов максимум 50 студентов
            if max_students > 50:
                cleaned_data['max_students'] = 50
        elif not is_online and max_students:
            # Для очных курсов максимум 30 студентов
            if max_students > 30:
                cleaned_data['max_students'] = 30
        
        # Если курс не имеет описания, генерируем автоматически
        if not cleaned_data.get('description') and cleaned_data.get('title'):
            title = cleaned_data.get('title')
            level = cleaned_data.get('level', 'beginner')
            level_dict = dict(Course.LEVEL_CHOICES)
            level_name = level_dict.get(level, 'Начинающий')
            
            cleaned_data['description'] = f"Курс «{title}». Уровень: {level_name}."
        
        # Автоматически добавляем prerequisites на основе уровня
        if not cleaned_data.get('prerequisites'):
            level = cleaned_data.get('level', 'beginner')
            prerequisites_map = {
                'beginner': 'Базовые знания предмета не требуются.',
                'intermediate': 'Рекомендуется пройти начальный курс.',
                'advanced': 'Необходимы знания среднего уровня.'
            }
            cleaned_data['prerequisites'] = prerequisites_map.get(level, '')
        
        # Проверка на отрицательную цену
        price = cleaned_data.get('price')
        if price is not None and price < 0:
            cleaned_data['price'] = 0
        
        return cleaned_data


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'email', 'phone', 
            'birth_date', 'student_id', 'group_number', 
            'gpa', 'scholarship', 'graduation_year'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'graduation_year': forms.NumberInput(attrs={'min': '2020', 'max': '2030'}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'phone': 'Телефон',
            'birth_date': 'Дата рождения',
            'student_id': 'Номер студенческого',
            'group_number': 'Номер группы',
            'gpa': 'Средний балл',
            'scholarship': 'Стипендия',
            'graduation_year': 'Год выпуска',
        }
    
    # Метод clean_first_name - форматирует имя
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            return format_name(first_name)
        return first_name
    
    # Метод clean_last_name - форматирует фамилию
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            return format_name(last_name)
        return last_name
    
    # Метод clean_email - приводит к нижнему регистру
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Приводим к нижнему регистру и убираем пробелы
            email = email.lower().strip()
            
            # Если email из распространенных ошибок, исправляем
            common_fixes = {
                'gmial.com': 'gmail.com',
                'gmal.com': 'gmail.com',
                'yandex.com': 'yandex.ru',
                'mail.com': 'mail.ru',
            }
            
            parts = email.split('@')
            if len(parts) == 2:
                username, domain = parts
                if domain in common_fixes:
                    email = f"{username}@{common_fixes[domain]}"
            
            return email
        return email
    
    # Метод clean_phone - валидирует и форматирует
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            validate_phone_format(phone)
            return format_phone(phone)
        return phone
    
    # Метод clean_gpa - автоматически корректирует и форматирует
    def clean_gpa(self):
        gpa = self.cleaned_data.get('gpa')
        if gpa is not None:
            # Округляем до 2 знаков
            gpa = round(gpa, 2)
            
            if gpa > 5.0:
                gpa = 5.0
            if gpa < 0:
                gpa = 0
            return gpa
        return gpa
    
    # Метод clean_student_id - форматирует номер студенческого
    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if student_id:
            # Убираем пробелы и приводим к верхнему регистру
            student_id = student_id.strip().upper()
            
            if not student_id.isalnum():
                raise ValidationError(
                    'Номер студенческого билета должен содержать только буквы и цифры.'
                )
            if len(student_id) < 5:
                raise ValidationError(
                    'Номер студенческого билета должен быть не менее 5 символов.'
                )
            return student_id
        return student_id
    
    # Метод clean_scholarship - форматирует стипендию
    def clean_scholarship(self):
        scholarship = self.cleaned_data.get('scholarship')
        if scholarship:
            # Округляем до 2 знаков
            scholarship = round(scholarship, 2)
            
            if scholarship < 0:
                scholarship = 0
            return scholarship
        return scholarship
    
    # Общий clean() для формы
    def clean(self):
        cleaned_data = super().clean()
        
        birth_date = cleaned_data.get('birth_date')
        graduation_year = cleaned_data.get('graduation_year')
        
        # Автоматически вычисляем год выпуска на основе возраста
        if birth_date and not graduation_year:
            # Предполагаем окончание в 22 года (бакалавриат)
            estimated_graduation = birth_date.year + 22
            # Проверяем, что год не в прошлом
            if estimated_graduation < date.today().year:
                estimated_graduation = date.today().year + 1
            cleaned_data['graduation_year'] = estimated_graduation
        
        # Проверка: год выпуска должен быть после года рождения
        if birth_date and graduation_year:
            if graduation_year <= birth_date.year:
                # Автоматически исправляем
                cleaned_data['graduation_year'] = birth_date.year + 22
        
        # Автоматически устанавливаем стипендию на основе GPA
        scholarship = cleaned_data.get('scholarship')
        gpa = cleaned_data.get('gpa')
        
        if gpa and gpa >= 4.5 and not scholarship:
            # Базовая стипендия при высоком GPA
            cleaned_data['scholarship'] = 2000
        
        if scholarship and scholarship > 0 and (gpa is None or gpa < 4.0):
            # Если GPA низкий, убираем стипендию
            cleaned_data['scholarship'] = 0
        
        # Если GPA отличный, увеличиваем стипендию автоматически
        if gpa and gpa >= 4.8 and scholarship:
            # Повышенная стипендия
            cleaned_data['scholarship'] = max(scholarship, 5000)
        
        # Автоматически генерируем группу, если не указана
        if not cleaned_data.get('group_number') and graduation_year:
            form = cleaned_data.get('form_of_study', 'О')
            cleaned_data['group_number'] = f"{graduation_year}-{form}01"
        
        return cleaned_data