from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager

class User(AbstractBaseUser):
    first_name = models.CharField(
        max_length=70,
    )
    last_name = models.CharField(
        max_length=70    
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # required fileds
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    class Meta:
        db_table = "ReserveSystem_accounts"
        # verbose_name = 'account'
        # verbose_popular_name = "accounts"

    def get_fullname(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def __str__(self) -> str:
        return self.get_fullname()
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin