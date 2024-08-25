from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()


class EmailAuthBackend:
    """Authenticate using an email adress"""

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return User
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            return None


def create_profile(backend, user, *args, **kwargs):
    """Create a user profile for social authentication """
    Profile.objects.get_or_create(user=user)
