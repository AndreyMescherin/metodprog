from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Кастомная модель пользователя
    """
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='группы',
        blank=True,
        help_text='Группы, к которым принадлежит пользователь.',
        related_name="custom_user_groups",
        related_query_name="custom_user_group",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='права доступа',
        blank=True,
        help_text='Специальные права для пользователя.',
        related_name="custom_user_permissions",
        related_query_name="custom_user_permission",
    )
    
    middle_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Отчество")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    
    # ImageField для аватара
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name="Аватар"
    )
    
    bio = models.TextField(blank=True, null=True, verbose_name="О себе")
    is_teacher = models.BooleanField(default=False, verbose_name="Преподаватель")
    is_student = models.BooleanField(default=False, verbose_name="Студент")
    
    friends = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=True,
        verbose_name="Друзья",
    )
    
    is_public = models.BooleanField(
        default=False,
        verbose_name="Публичный профиль",
        help_text="Если отмечено, профиль виден всем пользователям"
    )
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
    
    def __str__(self):
        if self.get_full_name():
            return self.get_full_name()
        return self.username
    
    def get_full_name_with_middle(self):
        parts = [self.last_name, self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        return ' '.join(p for p in parts if p)
    
    def get_friends(self):
        return self.friends.all()
    
    def get_friends_count(self):
        return self.friends.count()
    
    def add_friend(self, user):
        if user != self:
            self.friends.add(user)
            return True
        return False
    
    def remove_friend(self, user):
        self.friends.remove(user)
    
    def is_friend(self, user):
        return self.friends.filter(id=user.id).exists()
    
    def can_view_profile(self, user):
        if not user.is_authenticated:
            return False
        if user == self:
            return True
        if self.is_public:
            return True
        if self.is_friend(user):
            return True
        return False