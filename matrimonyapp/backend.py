from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import User

class CreatorIDBackend(BaseBackend):
    def authenticate(self, request, creator_id=None, password=None, **kwargs):
        try:
            user = User.objects.get(creator_id=creator_id)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
