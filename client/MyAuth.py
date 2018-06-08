from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from validation.models import Validation


class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password.
    """
    def authenticate(self, token=None):
        try:
            validation = Validation.objects.filter(keyValidation=token, estValider=0, estSupprimer=0)[0]
            validation.estValider = 1
            validation.estSupprimer = 1
            validation.save()
            user = User.objects.get(username=validation.client.user.username)#validation.client.user
            return user
        except User.DoesNotExist:
            return None
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None