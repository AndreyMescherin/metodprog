import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

logger = logging.getLogger('auth')


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Логирование успешного входа"""
    logger.info(f"User '{user.username}' logged in successfully from IP: {request.META.get('REMOTE_ADDR')}")


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """Логирование выхода"""
    if user:
        logger.info(f"User '{user.username}' logged out")
    else:
        logger.info("Anonymous user logged out")


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    """Логирование неудачного входа"""
    username = credentials.get('username', 'unknown')
    logger.warning(f"Failed login attempt for user '{username}' from IP: {request.META.get('REMOTE_ADDR')}")