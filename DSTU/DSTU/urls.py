from django.urls import path, include
from catalog import views
from django.contrib import admin

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('courses/', views.courses_list, name='courses'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('authors/', views.authors_list, name='authors'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
    path('info/', views.info, name='info'),
    path('schedule/', include('schedule.urls')),
]

handler404 = 'catalog.views.custom_404'
admin.site.site_header = 'Управление расписанием'
admin.site.site_title = 'Админ-панель расписания'
admin.site.index_title = 'Добро пожаловать в систему управления'