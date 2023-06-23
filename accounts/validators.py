import re
from django.core.exceptions import ValidationError

def is_valid_phone_number(phone_number):
    if not re.match(r'^09[0-9]{9}$', str(phone_number)):
        raise ValidationError('لطفا شماره موبایل معتبر وارد کنید.')
