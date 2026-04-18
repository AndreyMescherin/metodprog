from django.contrib import admin
from .models import Teacher, TeacherInfo, Course, Student

# Настройка отображения Teacher в админке
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone', 'hire_date', 'salary']
    list_display_links = ['first_name', 'last_name']
    list_filter = ['hire_date', 'salary']
    search_fields = ['first_name', 'last_name', 'email']
    list_editable = ['salary']
    fieldsets = (
        ('Основная информация', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Контактная информация', {
            'fields': ('phone',)
        }),
        ('Рабочая информация', {
            'fields': ('hire_date', 'salary')
        }),
    )

# Настройка отображения TeacherInfo в админке
@admin.register(TeacherInfo)
class TeacherInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'teacher', 'experience_years', 'education', 'office_number']
    list_filter = ['experience_years', 'education']
    search_fields = ['teacher__first_name', 'teacher__last_name', 'address']
    raw_id_fields = ['teacher']  # Удобный поиск при выборе преподавателя

# Настройка отображения Course в админке
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'teacher', 'level', 'credits', 'price', 'duration_weeks']
    list_filter = ['level', 'teacher', 'credits']
    search_fields = ['title', 'description', 'teacher__first_name', 'teacher__last_name']
    list_editable = ['price']
      # Для удобного выбора студентов
    fieldsets = (
        ('Информация о курсе', {
            'fields': ('title', 'description', 'level')
        }),
        ('Детали курса', {
            'fields': ('credits', 'duration_weeks', 'price')
        }),
        ('Преподаватель и студенты', {
            'fields': ('teacher', 'students')
        }),
    )

# Настройка отображения Student в админке
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone', 'enrollment_date', 'get_courses_count']
    list_filter = ['enrollment_date', 'courses']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    filter_horizontal = ['courses']  # Для удобного выбора курсов
    readonly_fields = ['enrollment_date']  # Поле только для чтения
    fieldsets = (
        ('Личная информация', {
            'fields': ('first_name', 'last_name', 'birth_date')
        }),
        ('Контактная информация', {
            'fields': ('email', 'phone')
        }),
        ('Учебная информация', {
            'fields': ('enrollment_date', 'courses')
        }),
    )
    
    def get_courses_count(self, obj):
        return obj.courses.count()
    get_courses_count.short_description = 'Количество курсов'
    get_courses_count.admin_order_field = 'courses__count'