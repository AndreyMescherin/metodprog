import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import CustomUserCreationForm, ProfileEditForm
from .models import User

# Создаем логгер для этого модуля
logger = logging.getLogger(__name__)
auth_logger = logging.getLogger('auth')


def register(request):
    """
    Регистрация нового пользователя
    """
    if request.user.is_authenticated:
        logger.info(f"Authenticated user {request.user.username} tried to access register page")
        return redirect('schedule:teacher_index')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Логирование успешной регистрации
            logger.info(f"New user registered: {user.username} (email: {user.email})")
            auth_logger.info(f"User {user.username} registered and logged in")
            
            messages.success(request, f'Добро пожаловать, {user.first_name}! Регистрация успешна.')
            return redirect('users:profile')
        else:
            # Логирование ошибок валидации
            logger.warning(f"Registration failed. Errors: {form.errors}")
            auth_logger.warning(f"Failed registration attempt with data: {form.data.get('username', 'unknown')}")
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    """Просмотр своего профиля"""
    logger.debug(f"User {request.user.username} viewing own profile")
    friends = request.user.get_friends()
    return render(request, 'registration/profile.html', {
        'profile_user': request.user,
        'friends': friends,
        'is_own_profile': True,
    })


@login_required
def profile_edit(request):
    """Редактирование профиля"""
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            logger.info(f"User {request.user.username} updated profile")
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('users:profile')
        else:
            logger.warning(f"Profile update failed for {request.user.username}: {form.errors}")
    else:
        form = ProfileEditForm(instance=request.user)
    
    return render(request, 'registration/profile_edit.html', {'form': form})


@login_required
def user_list(request):
    """Список всех пользователей"""
    users = User.objects.all().exclude(id=request.user.id)
    logger.debug(f"User {request.user.username} viewing user list ({users.count()} users)")
    return render(request, 'registration/user_list.html', {
        'users': users,
    })


@login_required
def user_detail(request, user_id):
    """Просмотр профиля другого пользователя"""
    profile_user = get_object_or_404(User, id=user_id)
    
    if not profile_user.can_view_profile(request.user):
        logger.warning(
            f"User {request.user.username} tried to view private profile of {profile_user.username}"
        )
        messages.error(request, 'У вас нет доступа к просмотру этого профиля.')
        return redirect('users:user_list')
    
    logger.info(f"User {request.user.username} viewing profile of {profile_user.username}")
    is_friend = profile_user.is_friend(request.user)
    friends = profile_user.get_friends()
    
    return render(request, 'registration/user_detail.html', {
        'profile_user': profile_user,
        'friends': friends,
        'is_friend': is_friend,
        'is_own_profile': request.user == profile_user,
    })


@login_required
def add_friend(request, user_id):
    """Добавить пользователя в друзья"""
    friend = get_object_or_404(User, id=user_id)
    
    if friend == request.user:
        logger.warning(f"User {request.user.username} tried to add self as friend")
        messages.error(request, 'Нельзя добавить себя в друзья.')
    elif request.user.is_friend(friend):
        logger.info(f"User {request.user.username} already friends with {friend.username}")
        messages.warning(request, f'{friend.get_full_name()} уже у вас в друзьях.')
    else:
        request.user.add_friend(friend)
        logger.info(f"User {request.user.username} added {friend.username} as friend")
        messages.success(request, f'{friend.get_full_name()} добавлен(а) в друзья!')
    
    return redirect('users:user_detail', user_id=user_id)


@login_required
def remove_friend(request, user_id):
    """Удалить пользователя из друзей"""
    friend = get_object_or_404(User, id=user_id)
    
    if request.user.is_friend(friend):
        request.user.remove_friend(friend)
        logger.info(f"User {request.user.username} removed {friend.username} from friends")
        messages.success(request, f'{friend.get_full_name()} удален(а) из друзей.')
    else:
        logger.warning(f"User {request.user.username} tried to remove non-friend {friend.username}")
        messages.warning(request, 'Этот пользователь не в вашем списке друзей.')
    
    return redirect('users:user_detail', user_id=user_id)


@login_required
def friends_list(request):
    """Список друзей"""
    friends = request.user.get_friends()
    logger.debug(f"User {request.user.username} viewing friends list ({friends.count()} friends)")
    return render(request, 'registration/friends_list.html', {
        'friends': friends,
    })


