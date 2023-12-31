from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, full_name, phone_number, password=None, *args, **kwargs):
        """
        Creates and saves a User with the given first_name, last_name,
        phone_number and password.
        """
        if not phone_number:
            raise ValueError("Users must have an phone_number address")

        user = self.model(
            full_name=full_name,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, phone_number, password=None, *args, **kwargs):
        """
        Creates and saves a superuser with the given first_name, last_name,
        phone_number and password.
        """
        user = self.create_user(
            full_name=full_name,
            phone_number=phone_number,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
