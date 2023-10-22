import os

from django.core.exceptions import ValidationError

def allow_only_validator(value):
    extention = os.path.splitext(value.name)[1]
    valid_extention = ['.png', '.jpg', '.jpeg']

    if not extention.lower() in valid_extention:
        raise ValidationError('Unsupported file extention. Allow extentions: ' + str(valid_extention))
