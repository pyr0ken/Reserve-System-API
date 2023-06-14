from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password, *args, **kwargs):
        """
        Creates and saves a User with the given first_name, last_name,
        email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password, *args, **kwargs):
        """
        Creates and saves a superuser with the given first_name, last_name,
        email and password.
        """
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
