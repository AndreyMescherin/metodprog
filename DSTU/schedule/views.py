from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Teacher, TeacherInfo, Course, Student
from .forms import TeacherForm, TeacherInfoForm, CourseForm, StudentForm


# ============== Teacher Views ==============

def teacher_index(request):
    """Главная страница преподавателей"""
    teachers = Teacher.objects.all()
    return render(request, 'schedule/teacher_index.html', {'teachers': teachers})


def teacher_list(request):
    """Список всех преподавателей"""
    teachers = Teacher.objects.all()
    return render(request, 'schedule/teacher_list.html', {'teachers': teachers})


def teacher_detail(request, pk):
    """Детальная информация о преподавателе"""
    teacher = get_object_or_404(Teacher, pk=pk)
    return render(request, 'schedule/teacher_detail.html', {'teacher': teacher})


def teacher_info(request, teacher_id):
    """Информация о преподавателе (альтернативный маршрут)"""
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    return render(request, 'schedule/teacher_detail.html', {'teacher': teacher})


def teacher_create(request):
    """Создание нового преподавателя"""
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save()
            
            if hasattr(form, '_warnings'):
                for warning in form._warnings:
                    messages.warning(request, warning)
            
            messages.success(request, 'Преподаватель успешно добавлен!')
            return redirect('schedule:teacher_index')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = TeacherForm()
    
    return render(request, 'schedule/teacher_form.html', {'form': form})


def teacher_update(request, teacher_id=None, pk=None):
    """Обновление данных преподавателя"""
    # Поддержка разных имен параметров из URL
    id_value = teacher_id or pk
    teacher = get_object_or_404(Teacher, pk=id_value)
    
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            
            if hasattr(form, '_warnings'):
                for warning in form._warnings:
                    messages.warning(request, warning)
            
            messages.success(request, 'Данные преподавателя обновлены!')
            return redirect('schedule:teacher_info', teacher_id=teacher.pk)
    else:
        form = TeacherForm(instance=teacher)
    
    return render(request, 'schedule/teacher_form.html', {'form': form})


def teacher_delete(request, teacher_id):
    """Удаление преподавателя"""
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'Преподаватель удален!')
        return redirect('schedule:teacher_index')
    return render(request, 'schedule/teacher_confirm_delete.html', {'teacher': teacher})


# ============== TeacherInfo Views ==============

def teacher_info_create(request, teacher_pk):
    """Добавление информации о преподавателе"""
    teacher = get_object_or_404(Teacher, pk=teacher_pk)
    
    if hasattr(teacher, 'info'):
        return redirect('teacher_info_update', teacher_pk=teacher.pk)
    
    if request.method == 'POST':
        form = TeacherInfoForm(request.POST)
        if form.is_valid():
            info = form.save(commit=False)
            info.teacher = teacher
            info.save()
            messages.success(request, 'Информация о преподавателе добавлена!')
            return redirect('schedule:teacher_info', teacher_id=teacher.pk)
    else:
        form = TeacherInfoForm()
    
    return render(request, 'schedule/teacher_info_form.html', {
        'form': form,
        'teacher': teacher
    })


def teacher_info_update(request, teacher_pk):
    """Обновление информации о преподавателе"""
    teacher = get_object_or_404(Teacher, pk=teacher_pk)
    info = getattr(teacher, 'info', None)
    
    if info is None:
        return redirect('teacher_info_create', teacher_pk=teacher.pk)
    
    if request.method == 'POST':
        form = TeacherInfoForm(request.POST, instance=info)
        if form.is_valid():
            form.save()
            messages.success(request, 'Информация о преподавателе обновлена!')
            return redirect('schedule:teacher_info', teacher_id=teacher.pk)
    else:
        form = TeacherInfoForm(instance=info)
    
    return render(request, 'schedule/teacher_info_form.html', {
        'form': form,
        'teacher': teacher
    })


# ============== Course Views ==============

def course_index(request):
    """Главная страница курсов"""
    courses = Course.objects.all()
    return render(request, 'schedule/course_index.html', {'courses': courses})


def course_list(request):
    """Список всех курсов"""
    courses = Course.objects.all()
    return render(request, 'schedule/course_list.html', {'courses': courses})


def course_detail(request, pk):
    """Детальная информация о курсе"""
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'schedule/course_detail.html', {'course': course})


def course_create(request):
    """Создание нового курса"""
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Курс успешно создан!')
            return redirect('schedule:course_index')
    else:
        form = CourseForm()
    
    return render(request, 'schedule/course_form.html', {'form': form})


def course_update(request, course_id):
    """Обновление курса"""
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Курс обновлен!')
            return redirect('schedule:course_index')
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'schedule/course_form.html', {'form': form})


def course_delete(request, course_id):
    """Удаление курса"""
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Курс удален!')
        return redirect('schedule:course_index')
    return render(request, 'schedule/course_confirm_delete.html', {'course': course})


# ============== Student Views ==============

def student_index(request):
    """Главная страница студентов"""
    students = Student.objects.all()
    return render(request, 'schedule/student_index.html', {'students': students})


def student_list(request):
    """Список всех студентов"""
    students = Student.objects.all()
    return render(request, 'schedule/student_list.html', {'students': students})


def student_detail(request, student_id):
    """Детальная информация о студенте"""
    student = get_object_or_404(Student, pk=student_id)
    return render(request, 'schedule/student_detail.html', {'student': student})


def student_create(request):
    """Добавление нового студента"""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Студент успешно зарегистрирован!')
            return redirect('schedule:student_index')
    else:
        form = StudentForm()
    
    return render(request, 'schedule/student_form.html', {'form': form})


def student_update(request, student_id):
    """Обновление данных студента"""
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные студента обновлены!')
            return redirect('schedule:student_detail', student_id=student.pk)
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'schedule/student_form.html', {'form': form})


def student_delete(request, student_id):
    """Удаление студента"""
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Студент удален!')
        return redirect('schedule:student_index')
    return render(request, 'schedule/student_confirm_delete.html', {'student': student})


def student_enroll(request, student_id):
    """Запись студента на курс"""
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        if course_id:
            course = get_object_or_404(Course, pk=course_id)
            student.courses.add(course)
            messages.success(request, f'Студент записан на курс "{course.title}"!')
    return redirect('schedule:student_detail', student_id=student_id)


def student_unenroll(request, student_id, course_id):
    """Отчисление студента с курса"""
    student = get_object_or_404(Student, pk=student_id)
    course = get_object_or_404(Course, pk=course_id)
    student.courses.remove(course)
    messages.success(request, f'Студент отчислен с курса "{course.title}"!')
    return redirect('schedule:student_detail', student_id=student_id)


# ============== ORM Queries ==============

def orm_queries(request):
    """Страница с примерами ORM запросов"""
    context = {
        'teachers': Teacher.objects.all(),
        'courses': Course.objects.all(),
        'students': Student.objects.all(),
    }
    return render(request, 'schedule/orm_queries.html', context) 