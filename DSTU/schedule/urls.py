from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    # Teacher URLs
    path('teachers/', views.teacher_index, name='teacher_index'),
    path('teachers/create/', views.teacher_create, name='teacher_create'),
    path('teachers/<int:teacher_id>/', views.teacher_info, name='teacher_info'),
    path('teachers/<int:teacher_id>/update/', views.teacher_update, name='teacher_update'),
    path('teachers/<int:teacher_id>/delete/', views.teacher_delete, name='teacher_delete'),
    
    # Course URLs
    path('courses/', views.course_index, name='course_index'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:course_id>/update/', views.course_update, name='course_update'),
    path('courses/<int:course_id>/delete/', views.course_delete, name='course_delete'),
    
    # Student URLs
    path('students/', views.student_index, name='student_index'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),
    path('students/<int:student_id>/update/', views.student_update, name='student_update'),
    path('students/<int:student_id>/delete/', views.student_delete, name='student_delete'),
    path('students/<int:student_id>/enroll/', views.student_enroll, name='student_enroll'),
    path('students/<int:student_id>/unenroll/<int:course_id>/', views.student_unenroll, name='student_unenroll'),
    
    # ORM Queries
    path('orm-queries/', views.orm_queries, name='orm_queries'),
]