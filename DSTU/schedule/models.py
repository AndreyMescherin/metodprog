from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

# Модель Teacher (преподаватель)
class Teacher(models.Model):
    # Обязательные поля (существующие)
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    hire_date = models.DateField(verbose_name="Дата найма")
    salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Зарплата",
        validators=[MinValueValidator(0)]
    )
    

    department = models.CharField(
        max_length=100, 
        verbose_name="Кафедра",
        blank=True,  # Можно оставить пустым в форме
        null=True,   # Может быть NULL в базе данных
        default=None  # По умолчанию None
    )
    
    academic_degree = models.CharField(
        max_length=50,
        verbose_name="Ученая степень",
        choices=[
            ('bachelor', 'Бакалавр'),
            ('master', 'Магистр'),
            ('phd', 'Кандидат наук'),
            ('doctor', 'Доктор наук'),
        ],
        blank=True,
        null=True,
        default=None
    )
    
    office_hours = models.CharField(
        max_length=100,
        verbose_name="Часы приема",
        blank=True,
        null=True,
        default=None,
        help_text="Например: Пн-Пт 10:00-12:00"
    )
    
    is_active = models.BooleanField(
        default=True,  # По умолчанию True для существующих записей
        verbose_name="Активен"
    )
    
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        verbose_name="Рейтинг",
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        blank=True,
        null=True,
        default=0  # По умолчанию 0
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
        unique_together = ['first_name', 'last_name', 'email']


class TeacherInfo(models.Model):
    # Существующие поля
    teacher = models.OneToOneField(
        Teacher, 
        on_delete=models.CASCADE,
        related_name='info',
        verbose_name="Преподаватель",
        null=True,
        blank=True
    )
    
    address = models.TextField(
        verbose_name="Адрес",
        null=True,
        blank=True
    )
    
    birth_date = models.DateField(
        verbose_name="Дата рождения",
        null=True,
        blank=True
    )
    
    education = models.CharField(
        max_length=200,
        verbose_name="Образование",
        null=True,
        blank=True
    )
    
    experience_years = models.PositiveIntegerField(
        default=0,
        verbose_name="Опыт работы (лет)",
        validators=[MaxValueValidator(50)],
        null=True,
        blank=True
    )
    
    bio = models.TextField(
        verbose_name="Биография",
        blank=True,
        null=True
    )
    
    office_number = models.CharField(
        max_length=10,
        verbose_name="Номер кабинета",
        blank=True,
        null=True
    )
    
    # НОВЫЕ ПОЛЯ - все необязательные
    passport_number = models.CharField(
        max_length=20,
        verbose_name="Серия и номер паспорта",
        blank=True,
        null=True,
        default=None,
        validators=[RegexValidator(
            r'^\d{4}\s?\d{6}$', 
            message='Введите паспорт в формате: 1234 567890'
        )]
    )
    
    marital_status = models.CharField(
        max_length=20,
        verbose_name="Семейное положение",
        choices=[
            ('single', 'Холост/Не замужем'),
            ('married', 'Женат/Замужем'),
            ('divorced', 'Разведен/Разведена'),
        ],
        blank=True,
        null=True,
        default=None
    )
    
    publications_count = models.PositiveIntegerField(
        default=0,  # По умолчанию 0 для существующих записей
        verbose_name="Количество публикаций",
        blank=True,
        null=True
    )
    
    emergency_contact = models.CharField(
        max_length=20,
        verbose_name="Экстренный контакт",
        blank=True,
        null=True,
        default=None
    )
    
    def __str__(self):
        if self.teacher:
            return f"Информация о {self.teacher}"
        return "Информация о преподавателе (без связи)"
    
    class Meta:
        verbose_name = "Информация о преподавателе"
        verbose_name_plural = "Информация о преподавателях"


class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Начинающий'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ]
    
    # Существующие поля
    title = models.CharField(max_length=100, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание")
    credits = models.PositiveIntegerField(
        verbose_name="Кредиты", 
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    level = models.CharField(
        max_length=20, 
        choices=LEVEL_CHOICES, 
        default='beginner', 
        verbose_name="Уровень"
    )
    duration_weeks = models.PositiveIntegerField(
        verbose_name="Длительность (недель)", 
        validators=[MinValueValidator(1)]
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Стоимость", 
        validators=[MinValueValidator(0)]
    )
    
    teacher = models.ForeignKey(
        Teacher, 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name='courses',
        verbose_name="Преподаватель"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    # НОВЫЕ ПОЛЯ - все необязательные или со значениями по умолчанию
    max_students = models.PositiveIntegerField(
        verbose_name="Максимальное количество студентов",
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        default=30,  # По умолчанию 30 для существующих курсов
        blank=True,
        null=True
    )
    
    syllabus = models.TextField(
        verbose_name="Учебный план",
        blank=True,
        null=True,
        default=None
    )
    
    prerequisites = models.TextField(
        verbose_name="Предварительные требования",
        blank=True,
        null=True,
        default=None
    )
    
    is_online = models.BooleanField(
        default=False,  # По умолчанию False (очные курсы)
        verbose_name="Онлайн курс"
    )
    
    start_date = models.DateField(
        verbose_name="Дата начала курса",
        blank=True,
        null=True,
        default=None
    )
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        unique_together = ['title', 'teacher']


class Student(models.Model):
    # Существующие поля
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    birth_date = models.DateField(verbose_name="Дата рождения")
    enrollment_date = models.DateField(auto_now_add=True, verbose_name="Дата зачисления")
    
    courses = models.ManyToManyField(
        Course, 
        related_name='students', 
        blank=True,
        verbose_name="Курсы"
    )
    
    # НОВЫЕ ПОЛЯ - все необязательные или со значениями по умолчанию
    student_id = models.CharField(
        max_length=20,
        verbose_name="Номер студенческого билета",
        unique=True,  # Уникальное поле
        blank=True,
        null=True,
        default=None
    )
    
    group_number = models.CharField(
        max_length=10,
        verbose_name="Номер группы",
        blank=True,
        null=True,
        default=None
    )
    
    gpa = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        verbose_name="Средний балл",
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        blank=True,
        null=True,
        default=None
    )
    
    scholarship = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стипендия",
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        default=0  # По умолчанию 0 (без стипендии)
    )
    
    graduation_year = models.PositiveIntegerField(
        verbose_name="Год выпуска",
        blank=True,
        null=True,
        default=None,
        validators=[MinValueValidator(2020), MaxValueValidator(2030)]
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        unique_together = ['first_name', 'last_name', 'email']