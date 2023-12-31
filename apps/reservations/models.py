from turtle import mode
from django.db import models
from django.conf import settings


class SonsTimes(models.Model):
    time = models.TimeField()
    price = models.DecimalField(decimal_places=0, max_digits=10,
                                help_text="قیمت را به <strong>تومان</strong> وارد کنید.")
    holiday_price = models.DecimalField(decimal_places=0, max_digits=10,
                                        help_text="قیمت را به <strong>تومان</strong> وارد کنید.")

    class Meta:
        verbose_name = "Sons Time"
        verbose_name_plural = "Sons Times"
        ordering = ['time']
        db_table = "ReserveSystem_sons_times"

    def __str__(self):
        return f'time:{self.time} - price:{self.price}'


class Reservations(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_reserves")
    sons_time = models.ForeignKey(to=SonsTimes, on_delete=models.CASCADE, related_name="sons_time_reserves")
    date = models.DateField()
    time = models.TimeField()
    price = models.DecimalField(decimal_places=0, max_digits=10)
    count = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ReserveSystem_reservations"

    def __str__(self):
        return f"user:{self.user} - created:{self.created_at}"


class Transactions(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_transactions")
    reservation = models.ForeignKey(to=Reservations, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=0, max_digits=20)
    is_paid = models.BooleanField(default=False)
    authority = models.BigIntegerField(null=True, blank=True)
    RefID = models.BigIntegerField(null=True, blank=True)
