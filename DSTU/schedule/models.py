from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Модель Teacher (преподаватель)
class Teacher(models.Model):
    # Обязательные поля
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="Email")  # unique - уникальное поле
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    hire_date = models.DateField(verbose_name="Дата найма")
    salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Зарплата",
        validators=[MinValueValidator(0)]  # ограничение: зарплата не может быть отрицательной
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
        # уникальность ФИО + email (ограничение повторных записей)
        unique_together = ['first_name', 'last_name', 'email']


# Модель TeacherInfo (дополнительная информация о преподавателе) - связь 1:1
class TeacherInfo(models.Model):
    # Связь 1:1 с Teacher (обязательная, но можно сделать необязательной)
    teacher = models.OneToOneField(
        Teacher, 
        on_delete=models.CASCADE,
        related_name='info',
        verbose_name="Преподаватель",
        null=True,  # Добавьте - разрешает NULL в БД
        blank=True   # Добавьте - разрешает пустое значение в формах
    )
    
    # Дополнительные поля - теперь все НЕОБЯЗАТЕЛЬНЫЕ
    address = models.TextField(
        verbose_name="Адрес",
        null=True,      # Разрешает NULL в БД
        blank=True      # Разрешает пустое значение в формах
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
        default=0,  # Значение по умолчанию
        verbose_name="Опыт работы (лет)",
        validators=[MaxValueValidator(50)],
        null=True,
        blank=True
    )
    
    bio = models.TextField(
        verbose_name="Биография",
        blank=True,  # blank=True уже есть, добавим null=True
        null=True
    )
    
    office_number = models.CharField(
        max_length=10,
        verbose_name="Номер кабинета",
        blank=True,
        null=True
    )
    
    def __str__(self):
        if self.teacher:
            return f"Информация о {self.teacher}"
        return "Информация о преподавателе (без связи)"
    
    class Meta:
        verbose_name = "Информация о преподавателе"
        verbose_name_plural = "Информация о преподавателях"


# Модель Course (курс) - связь 1:N с Teacher
class Course(models.Model):
    # Уровни курса
    LEVEL_CHOICES = [
        ('beginner', 'Начинающий'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ]
    
    # Обязательные поля
    title = models.CharField(max_length=100, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание")
    credits = models.PositiveIntegerField(verbose_name="Кредиты", validators=[MinValueValidator(1), MaxValueValidator(10)])
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner', verbose_name="Уровень")
    duration_weeks = models.PositiveIntegerField(verbose_name="Длительность (недель)", validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость", validators=[MinValueValidator(0)])
    
    # Связь 1:N с Teacher. При удалении Teacher - SET NULL (преподаватель удален, но курс остается)
    teacher = models.ForeignKey(
        Teacher, 
        on_delete=models.SET_NULL,  # SET NULL - при удалении учителя, у курса teacher становится NULL
        null=True, 
        blank=True,
        related_name='courses',
        verbose_name="Преподаватель"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        unique_together = ['title', 'teacher']  # ограничение: один учитель не может вести два одинаковых курса


# Модель Student (студент) - связь N:N с Course
class Student(models.Model):
    # Обязательные поля
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="Email")  # unique - уникальное поле
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    birth_date = models.DateField(verbose_name="Дата рождения")
    enrollment_date = models.DateField(auto_now_add=True, verbose_name="Дата зачисления")
    
    # Связь N:N с Course. При удалении курса - SET NULL (студент остается без курса)
    courses = models.ManyToManyField(
        Course, 
        related_name='students', 
        blank=True,
        verbose_name="Курсы"
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        unique_together = ['first_name', 'last_name', 'email']  # ограничение повторных записей