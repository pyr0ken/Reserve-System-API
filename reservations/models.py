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
    date = models.DateField()
    time = models.TimeField()
    price = models.DecimalField(decimal_places=0, max_digits=10)
    authority = models.CharField(max_length=200)
    RfID = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ReserveSystem_reservations"

    def __str__(self):
        return f"user:{self.user} - created:{self.created_at}"

# class Transactions(models.Model):
#     payment_id = models.CharField(max_length=32, unique=True)
#     sons_time = models.ForeignKey('SonsTimes', on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     id_card = models.CharField(max_length=255)
#     phone = models.CharField(max_length=255)
#     date = models.CharField(max_length=255)
#     price = models.PositiveBigIntegerField()
#     status = models.PositiveSmallIntegerField(default=1)  # 1 pending pay, 0 failure, 2 success
#     sessions = models.IntegerField(null=True)
#     transactionId = models.CharField(max_length=255, null=True)
#     referenceId = models.CharField(max_length=255, null=True)
#     invoice_details = models.TextField(null=True)
#     transaction_result = models.TextField(null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
