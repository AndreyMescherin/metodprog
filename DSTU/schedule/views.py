from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count
from .models import Teacher, TeacherInfo, Course, Student
from .forms import TeacherForm, TeacherInfoForm, CourseForm, StudentForm

# ==================== TEACHER VIEWS ====================

def teacher_index(request):
    """Index - список всех преподавателей"""
    teachers = Teacher.objects.all()
    return render(request, 'schedule/teacher_index.html', {'teachers': teachers})

def teacher_info(request, teacher_id):
    """Просмотр подробной информации о преподавателе"""
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher_info = TeacherInfo.objects.filter(teacher=teacher).first()
    courses = teacher.courses.all()
    return render(request, 'schedule/teacher_info.html', {
        'teacher': teacher,
        'teacher_info': teacher_info,
        'courses': courses
    })

def teacher_create(request):
    """Создание преподавателя с использованием TeacherForm (forms.Form)"""
    if request.method == 'POST':
        teacher_form = TeacherForm(request.POST)
        info_form = TeacherInfoForm(request.POST)
        
        if teacher_form.is_valid():
            # Создаем преподавателя из cleaned_data
            teacher = Teacher.objects.create(
                first_name=teacher_form.cleaned_data['first_name'],
                last_name=teacher_form.cleaned_data['last_name'],
                email=teacher_form.cleaned_data['email'],
                phone=teacher_form.cleaned_data.get('phone', ''),
                hire_date=teacher_form.cleaned_data['hire_date'],
                salary=teacher_form.cleaned_data.get('salary', 0)
            )
            
            # Сохраняем дополнительную информацию, если она заполнена
            if info_form.is_valid() and any(info_form.cleaned_data.values()):
                teacher_info = info_form.save(commit=False)
                teacher_info.teacher = teacher
                teacher_info.save()
                messages.success(request, f'Преподаватель {teacher} успешно создан с дополнительной информацией!')
            else:
                messages.success(request, f'Преподаватель {teacher} успешно создан!')
            
            return redirect('schedule:teacher_index')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        teacher_form = TeacherForm()
        info_form = TeacherInfoForm()
    
    return render(request, 'schedule/teacher_form.html', {
        'teacher_form': teacher_form,
        'info_form': info_form,
        'title': 'Добавление преподавателя'
    })

def teacher_update(request, teacher_id):
    """Обновление преподавателя и его информации"""
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher_info, created = TeacherInfo.objects.get_or_create(teacher=teacher)
    
    if request.method == 'POST':
        teacher_form = TeacherForm(request.POST, instance=teacher)
        info_form = TeacherInfoForm(request.POST, instance=teacher_info)
        
        if teacher_form.is_valid() and info_form.is_valid():
            teacher = teacher_form.save()
            teacher_info = info_form.save(commit=False)
            teacher_info.teacher = teacher
            teacher_info.save()
            messages.success(request, f'Преподаватель {teacher} успешно обновлен!')
            return redirect('schedule:teacher_index')  # ← ИСПРАВЛЕНО
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        teacher_form = TeacherForm(instance=teacher)
        info_form = TeacherInfoForm(instance=teacher_info)
    
    return render(request, 'schedule/teacher_form.html', {
        'teacher_form': teacher_form,
        'info_form': info_form,
        'title': 'Редактирование преподавателя'
    })

def teacher_delete(request, teacher_id):
    """Удаление преподавателя вместе с информацией о нем"""
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        teacher_name = str(teacher)
        teacher.delete()
        messages.success(request, f'Преподаватель {teacher_name} удален!')
        return redirect('schedule:teacher_index')  # ← ИСПРАВЛЕНО
    
    return render(request, 'schedule/confirm_delete.html', {
        'object': teacher,
        'type': 'преподавателя'
    })

# ==================== COURSE VIEWS ====================

def course_index(request):
    """Index курсов с фильтрацией по преподавателю"""
    teacher_filter = request.GET.get('teacher')
    if teacher_filter:
        courses = Course.objects.filter(teacher_id=teacher_filter)
    else:
        courses = Course.objects.all()
    
    teachers = Teacher.objects.all()
    return render(request, 'schedule/course_index.html', {
        'courses': courses,
        'teachers': teachers,
        'selected_teacher': teacher_filter
    })

def course_create(request):
    """Создание курса с выбором преподавателя"""
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, f'Курс "{course.title}" успешно создан!')
            return redirect('schedule:course_index')  # ← ИСПРАВЛЕНО
    else:
        form = CourseForm()
    
    return render(request, 'schedule/course_form.html', {
        'form': form,
        'title': 'Создание курса'
    })

def course_update(request, course_id):
    """Обновление курса"""
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save()
            messages.success(request, f'Курс "{course.title}" успешно обновлен!')
            return redirect('schedule:course_index')  # ← ИСПРАВЛЕНО
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'schedule/course_form.html', {
        'form': form,
        'title': 'Редактирование курса'
    })

def course_delete(request, course_id):
    """Удаление курса"""
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course_title = course.title
        course.delete()
        messages.success(request, f'Курс "{course_title}" удален!')
        return redirect('schedule:course_index')  # ← ИСПРАВЛЕНО
    
    return render(request, 'schedule/confirm_delete.html', {
        'object': course,
        'type': 'курс'
    })

# ==================== STUDENT VIEWS ====================

def student_index(request):
    """Index студентов"""
    students = Student.objects.all()
    return render(request, 'schedule/student_index.html', {'students': students})

def student_create(request):
    """Создание нового студента"""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Студент {student.first_name} {student.last_name} успешно создан!')
            return redirect('schedule:student_index')  # ← ИСПРАВЛЕНО
    else:
        form = StudentForm()
    
    return render(request, 'schedule/student_form.html', {
        'form': form,
        'title': 'Добавление студента'
    })

def student_detail(request, student_id):
    """Детальная информация о студенте"""
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'schedule/student_detail.html', {'student': student})

def student_update(request, student_id):
    """Обновление информации о студенте"""
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Студент {student.first_name} {student.last_name} успешно обновлен!')
            return redirect('schedule:student_index')  # ← ИСПРАВЛЕНО
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'schedule/student_form.html', {
        'form': form,
        'title': 'Редактирование студента'
    })

def student_delete(request, student_id):
    """Удаление студента"""
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student_name = str(student)
        student.delete()
        messages.success(request, f'Студент {student_name} удален!')
        return redirect('schedule:student_index')  # ← ИСПРАВЛЕНО
    
    return render(request, 'schedule/confirm_delete.html', {
        'object': student,
        'type': 'студента'
    })

def student_enroll(request, student_id):
    """Запись студента на курс"""
    student = get_object_or_404(Student, id=student_id)
    available_courses = Course.objects.exclude(students=student)
    
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        if course_id:
            course = get_object_or_404(Course, id=course_id)
            student.courses.add(course)
            messages.success(request, f'Студент {student.first_name} {student.last_name} записан на курс "{course.title}"!')
            return redirect('schedule:student_detail', student_id=student.id)  # ← ИСПРАВЛЕНО
    
    return render(request, 'schedule/student_enroll.html', {
        'student': student,
        'courses': available_courses
    })

def student_unenroll(request, student_id, course_id):
    """Отписка студента от курса"""
    student = get_object_or_404(Student, id=student_id)
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        student.courses.remove(course)
        messages.success(request, f'Студент {student.first_name} {student.last_name} отписан от курса "{course.title}"!')
    
    return redirect('schedule:student_detail', student_id=student.id)  # ← ИСПРАВЛЕНО

# ==================== ORM QUERIES ====================

# from django.shortcuts import render
# from django.db.models import Count, Q
# from .models import Teacher, TeacherInfo, Course, Student

def orm_queries(request):
    """Страница с результатами ORM-запросов"""
    
    # 1. Все студенты первого курса
    first_course = Course.objects.first()
    students_of_course = first_course.students.all() if first_course else []
    
    # 2. Преподаватели, у которых больше 2 курсов
    teachers_with_many_courses = Teacher.objects.annotate(
        course_count=Count('courses')
    ).filter(course_count__gt=2)
    
    # 3. Студенты без курсов
    students_without_courses = Student.objects.filter(courses__isnull=True)
    
    # 4. Преподаватели без профиля
    teachers_without_profile = Teacher.objects.filter(info__isnull=True)
    
    # 5. ПОПУЛЯРНЫЕ КУРСЫ (больше 3 студентов)
    # Это запрос, который вы просили добавить
    popular_courses = Course.objects.annotate(
        student_count=Count('students')
    ).filter(student_count__gt=3)
    
    # 6. СТУДЕНТЫ, ЗАПИСАННЫЕ НА КУРСЫ КОНКРЕТНОГО ПРЕПОДАВАТЕЛЯ
    # Для примера берем первого преподавателя (или можно передать ID)
    example_teacher = Teacher.objects.first()
    students_of_teacher_courses = Student.objects.none()  # Пустой QuerySet по умолчанию
    
    if example_teacher:
        # Находим всех студентов, которые записаны на курсы этого преподавателя
        students_of_teacher_courses = Student.objects.filter(
            courses__teacher=example_teacher
        ).distinct()  # distinct() чтобы избежать дубликатов, если студент на нескольких курсах

    context = {
        # Существующие запросы
        'first_course': first_course,
        'students_of_course': students_of_course,
        'teachers_with_many_courses': teachers_with_many_courses,
        'students_without_courses': students_without_courses,
        'teachers_without_profile': teachers_without_profile, 
        'popular_courses': popular_courses,
    'example_teacher': example_teacher,
    'students_of_teacher_courses': students_of_teacher_courses,
    }

    return render(request, 'schedule/orm_queries.html', context)